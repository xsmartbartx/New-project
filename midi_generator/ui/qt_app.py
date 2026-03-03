from __future__ import annotations

from pathlib import Path

from PySide6 import QtCore, QtWidgets

from ..config import settings
from ..core.generator import run as run_generator
from ..core.types import Preset, TimeSignature


class GeneratorWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MIDI & Drum Pattern Generator")
        self.setMinimumWidth(520)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()

        # Musical section
        self.genre = QtWidgets.QComboBox()
        self.genre.addItems(sorted(settings.PROGRESSION_PRESETS.keys()))

        self.mood = QtWidgets.QComboBox()
        self.mood.addItems(settings.SUPPORTED_MOODS)

        self.scale = QtWidgets.QComboBox()
        self.scale.addItems(sorted(settings.SCALES.keys()))

        self.key = QtWidgets.QComboBox()
        for name in settings.NOTE_NAME_TO_SEMITONE.keys():
            self.key.addItem(name)
        self.key.setCurrentText("A")

        self.bpm = QtWidgets.QSpinBox()
        self.bpm.setRange(40, 240)
        self.bpm.setValue(140)

        self.bars = QtWidgets.QSpinBox()
        self.bars.setRange(1, 128)
        self.bars.setValue(8)

        self.time_sig = QtWidgets.QComboBox()
        for ts in ("4/4", "3/4", "6/8"):
            self.time_sig.addItem(ts)
        self.time_sig.setCurrentText("4/4")

        self.chord_mode = QtWidgets.QComboBox()
        self.chord_mode.addItems(settings.SUPPORTED_CHORD_MODES)

        form.addRow("Genre", self.genre)
        form.addRow("Mood", self.mood)
        form.addRow("Scale", self.scale)
        form.addRow("Key", self.key)
        form.addRow("BPM", self.bpm)
        form.addRow("Bars", self.bars)
        form.addRow("Time Signature", self.time_sig)
        form.addRow("Chord mode", self.chord_mode)

        # Groove section
        groove_box = QtWidgets.QGroupBox("Groove & Humanization")
        groove_layout = QtWidgets.QFormLayout(groove_box)

        self.complexity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.complexity.setRange(0, 100)
        self.complexity.setValue(50)

        self.swing = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.swing.setRange(0, 100)
        self.swing.setValue(0)

        self.humanize_ms = QtWidgets.QSpinBox()
        self.humanize_ms.setRange(0, 40)
        self.humanize_ms.setValue(8)

        self.humanize_vel = QtWidgets.QSpinBox()
        self.humanize_vel.setRange(0, 40)
        self.humanize_vel.setValue(12)

        groove_layout.addRow("Complexity", self.complexity)
        groove_layout.addRow("Swing %", self.swing)
        groove_layout.addRow("Timing humanize (ms)", self.humanize_ms)
        groove_layout.addRow("Velocity humanize", self.humanize_vel)

        # Output / seed
        self.seed = QtWidgets.QSpinBox()
        self.seed.setRange(0, 2**31 - 1)
        self.seed.setValue(7)

        self.output_dir = QtWidgets.QLineEdit(str(Path("output").resolve()))
        browse_btn = QtWidgets.QPushButton("Browse…")
        browse_btn.clicked.connect(self._choose_output_dir)
        out_layout = QtWidgets.QHBoxLayout()
        out_layout.addWidget(self.output_dir)
        out_layout.addWidget(browse_btn)

        self.combined = QtWidgets.QCheckBox("Also write combined.mid")

        form.addRow("Seed", self.seed)
        form.addRow("Output directory", out_layout)
        form.addRow("", self.combined)

        layout.addLayout(form)
        layout.addWidget(groove_box)

        # Status + buttons
        self.status = QtWidgets.QLabel("Ready.")
        self.status.setWordWrap(True)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        self.generate_btn = QtWidgets.QPushButton("Generate MIDI")
        self.generate_btn.clicked.connect(self._on_generate_clicked)
        btn_layout.addWidget(self.generate_btn)

        layout.addWidget(self.status)
        layout.addLayout(btn_layout)

    def _choose_output_dir(self) -> None:
        current = Path(self.output_dir.text())
        base = str(current if current.is_dir() else Path.cwd())
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select output folder", base)
        if directory:
            self.output_dir.setText(directory)

    def _current_preset(self) -> Preset:
        num, den = self.time_sig.currentText().split("/")
        ts = TimeSignature(numerator=int(num), denominator=int(den))
        return Preset(
            genre=self.genre.currentText(),
            scale=self.scale.currentText(),
            key=self.key.currentText(),
            bpm=int(self.bpm.value()),
            bars=int(self.bars.value()),
            time_signature=ts,
            mood=self.mood.currentText(),
            chord_mode=self.chord_mode.currentText(),
            complexity=self.complexity.value() / 100.0,
            swing=float(self.swing.value()),
            humanize_ms=float(self.humanize_ms.value()),
            humanize_velocity=int(self.humanize_vel.value()),
            seed=int(self.seed.value()),
            output_dir=Path(self.output_dir.text()),
            combined=self.combined.isChecked(),
        )

    @QtCore.Slot()
    def _on_generate_clicked(self) -> None:
        self.generate_btn.setEnabled(False)
        self.status.setText("Generating MIDI…")
        QtWidgets.QApplication.processEvents()

        try:
            preset = self._current_preset()
            out_dir = run_generator(preset)
        except Exception as exc:  # pragma: no cover - UI error path
            self.status.setText(f"Error: {exc}")
        else:
            msg = f"Generated MIDI files in: {out_dir.resolve()}"
            if preset.combined:
                msg += " (chords.mid, melody.mid, bass.mid, drums.mid, combined.mid)"
            else:
                msg += " (chords.mid, melody.mid, bass.mid, drums.mid)"
            self.status.setText(msg)
        finally:
            self.generate_btn.setEnabled(True)


def run() -> None:
    app = QtWidgets.QApplication([])
    w = GeneratorWindow()
    w.show()
    app.exec()


if __name__ == "__main__":  # pragma: no cover - manual launch
    run()

