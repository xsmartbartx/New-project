import unittest


class TestTheory(unittest.TestCase):
    def test_parse_key(self) -> None:
        from midi_generator.theory.scales import parse_key

        self.assertEqual(parse_key("C"), 0)
        self.assertEqual(parse_key("A"), 9)
        self.assertEqual(parse_key("Bb"), 10)

    def test_scale_pitch_classes(self) -> None:
        from midi_generator.theory.scales import scale_pitch_classes

        pcs = scale_pitch_classes(9, "minor")  # A minor
        self.assertIn(9, pcs)
        self.assertEqual(len(pcs), 7)


if __name__ == "__main__":
    unittest.main()

