-- Minimal relational schema (SQLite/Postgres compatible-ish).
-- Use as a starting point for full persistence described in CONTEXT.md.

CREATE TABLE IF NOT EXISTS presets (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  preset_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS generations (
  id TEXT PRIMARY KEY,
  preset_id TEXT NOT NULL,
  status TEXT NOT NULL,
  engine_version TEXT NOT NULL,
  requested_at TEXT NOT NULL,
  completed_at TEXT,
  output_dir TEXT,
  error_message TEXT,
  FOREIGN KEY (preset_id) REFERENCES presets(id)
);

