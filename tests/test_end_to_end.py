import os
import shutil
import tempfile
import unittest
from pathlib import Path


class TestEndToEnd(unittest.TestCase):
    def test_generates_midi_files(self) -> None:
        from midi_generator.core.types import Preset
        from midi_generator.core.generator import run

        tmp = Path(tempfile.mkdtemp(prefix="midi_gen_"))
        try:
            preset = Preset(output_dir=tmp, combined=True, seed=42)
            out_dir = run(preset)
            self.assertTrue((out_dir / "chords.mid").exists())
            self.assertTrue((out_dir / "melody.mid").exists())
            self.assertTrue((out_dir / "bass.mid").exists())
            self.assertTrue((out_dir / "drums.mid").exists())
            self.assertTrue((out_dir / "combined.mid").exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()

