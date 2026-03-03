from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

from ..core.types import Preset, TimeSignature


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def init_sqlite(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    schema_path = Path(__file__).with_name("schema.sql")
    conn.executescript(schema_path.read_text(encoding="utf-8"))
    return conn


def _preset_to_json(preset: Preset) -> str:
    d = asdict(preset)
    # Path is not JSON serializable
    d["output_dir"] = str(preset.output_dir)
    # TimeSignature is nested dataclass; asdict already converts it.
    return json.dumps(d, sort_keys=True)


def _preset_from_json(s: str) -> Preset:
    d = json.loads(s)
    ts = d.get("time_signature") or {}
    return Preset(
        genre=d["genre"],
        scale=d["scale"],
        key=d["key"],
        bpm=int(d["bpm"]),
        bars=int(d["bars"]),
        time_signature=TimeSignature(numerator=int(ts.get("numerator", 4)), denominator=int(ts.get("denominator", 4))),
        mood=d["mood"],
        chord_mode=d["chord_mode"],
        complexity=float(d["complexity"]),
        swing=float(d["swing"]),
        humanize_ms=float(d["humanize_ms"]),
        humanize_velocity=int(d["humanize_velocity"]),
        seed=int(d["seed"]),
        output_dir=Path(d["output_dir"]),
        combined=bool(d["combined"]),
    )


def save_preset(conn: sqlite3.Connection, preset: Preset, name: str, description: str = "") -> str:
    preset_id = str(uuid.uuid4())
    now = _now_iso()
    conn.execute(
        "INSERT INTO presets (id, name, description, preset_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (preset_id, name, description, _preset_to_json(preset), now, now),
    )
    conn.commit()
    return preset_id


def load_preset(conn: sqlite3.Connection, preset_id: str) -> Preset:
    row = conn.execute("SELECT preset_json FROM presets WHERE id = ?", (preset_id,)).fetchone()
    if not row:
        raise KeyError(f"Preset not found: {preset_id}")
    return _preset_from_json(row[0])


def create_generation(
    conn: sqlite3.Connection,
    preset_id: str,
    status: str,
    engine_version: str,
    output_dir: Optional[str],
    error_message: Optional[str] = None,
) -> str:
    gen_id = str(uuid.uuid4())
    now = _now_iso()
    conn.execute(
        "INSERT INTO generations (id, preset_id, status, engine_version, requested_at, completed_at, output_dir, error_message) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (gen_id, preset_id, status, engine_version, now, now, output_dir, error_message),
    )
    conn.commit()
    return gen_id


def latest_generation(conn: sqlite3.Connection) -> Optional[Tuple[str, str, str]]:
    row = conn.execute(
        "SELECT id, preset_id, status FROM generations ORDER BY requested_at DESC LIMIT 1"
    ).fetchone()
    if not row:
        return None
    return (row[0], row[1], row[2])

