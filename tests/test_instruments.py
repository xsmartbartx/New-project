import unittest


class TestInstruments(unittest.TestCase):
    def test_deterministic_seed(self) -> None:
        from midi_generator.core.types import Preset
        from midi_generator.core.generator import generate_patterns

        p1 = Preset(seed=123)
        p2 = Preset(seed=123)
        parts1 = generate_patterns(p1)
        parts2 = generate_patterns(p2)
        self.assertEqual(parts1["melody"], parts2["melody"])
        self.assertEqual(parts1["bass"], parts2["bass"])
        self.assertEqual(parts1["drums"], parts2["drums"])


if __name__ == "__main__":
    unittest.main()

