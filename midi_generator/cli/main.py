"""
CLI front-end for the MIDI & drum pattern generator.

Currently this module simply re-uses the existing implementation from
`generator.py` to keep behavior 1:1 while the internals are refactored into
the `midi_generator` package.
"""

from __future__ import annotations

import generator


def main() -> None:
    """Delegate to the legacy top-level main function."""
    generator.legacy_main()


__all__ = ["main"]

