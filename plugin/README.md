## MIDI & Drum Pattern Generator – Plugin (VST3 / AU)

This folder contains the **JUCE-based plugin** variant of the generator.
The goal is to ship native **VST3** and **Audio Unit (AU)** binaries that can
be loaded directly in DAWs, alongside the Python desktop app.

### Overview

- **Format targets**
  - VST3 (macOS and Windows)
  - Audio Unit (AUv2) on macOS
- **Host usage**
  - Insert as a **MIDI effect** or instrument, depending on host.
  - Use the plugin UI to control the same musical parameters as the Python app.
  - Route the plugin’s MIDI output into other tracks/instruments in the DAW.

The JUCE project is intentionally kept thin and delegates generation logic to a
shared core (re-implemented in C++ or bridged to the Python generator in a
separate process).

---

## Project Layout

```text
plugin/
├── CMakeLists.txt          # JUCE CMake project for VST3/AU
├── src/
│   ├── PluginProcessor.h   # AudioProcessor subclass
│   ├── PluginProcessor.cpp
│   ├── PluginEditor.h      # AudioProcessorEditor subclass
│   └── PluginEditor.cpp
└── README.md               # This file
```

---

## Build (JUCE + CMake)

### Prerequisites

- JUCE (6 or 7) checked out somewhere on your machine.
- CMake (>=3.15).
- A compiler toolchain:
  - macOS: Xcode or Clang
  - Windows: Visual Studio 2019+ with C++ workload

### Configure

From the repository root:

```bash
mkdir -p plugin/build
cd plugin/build

cmake .. \
  -DJUCE_DIR=/path/to/JUCE \
  -DCMAKE_BUILD_TYPE=Release
```

Replace `/path/to/JUCE` with the path to your JUCE checkout (where the
`CMakeLists.txt` for JUCE lives).

### Build

```bash
cmake --build . --config Release
```

This will produce:

- On macOS:
  - `MidiDrumGenerator.vst3`
  - `MidiDrumGenerator.component` (AUv2)
- On Windows:
  - `MidiDrumGenerator.vst3`

Exact paths depend on CMake generator and platform; typically under
`plugin/build/MidiDrumGenerator_artefacts/`.

---

## Installation

### macOS

Copy built binaries into standard plugin folders:

```bash
# VST3
sudo cp -R MidiDrumGenerator_artefacts/Release/VST3/MidiDrumGenerator.vst3 \
  "/Library/Audio/Plug-Ins/VST3/"

# Audio Unit
sudo cp -R MidiDrumGenerator_artefacts/Release/AU/MidiDrumGenerator.component \
  "/Library/Audio/Plug-Ins/Components/"
```

Then restart your DAW and rescan plugins if needed.

### Windows

Copy the VST3 into the common VST3 folder:

```powershell
Copy-Item `
  "MidiDrumGenerator_artefacts\Release\VST3\MidiDrumGenerator.vst3" `
  "C:\Program Files\Common Files\VST3\" -Recurse
```

Restart the DAW and trigger a plugin rescan.

---

## Installer Workflow (Planned)

To provide a smooth installation experience:

- **macOS**
  - Create a `.pkg` installer that:
    - Installs `MidiDrumGenerator.vst3` into `/Library/Audio/Plug-Ins/VST3/`.
    - Installs `MidiDrumGenerator.component` into `/Library/Audio/Plug-Ins/Components/`.
    - Optionally installs the Python desktop app into `/Applications/MidiDrumGenerator.app`
      or a user folder, and adds a shortcut.
- **Windows**
  - Create an `.msi` or `.exe` installer (WiX, Inno Setup, NSIS) that:
    - Installs `MidiDrumGenerator.vst3` into `C:\Program Files\Common Files\VST3\`.
    - Optionally installs the Python desktop app and a Start Menu shortcut.

These installers can be wired into a CI pipeline (GitHub Actions, etc.) that:

1. Builds the plugin in Release mode for each platform.
2. Packages the binaries into installers.
3. Uploads the installers as release assets.

---

## DAW Integration Notes

- **MIDI routing**
  - In most DAWs, insert the plugin on a MIDI track and route its MIDI output
    to an instrument track (or use it directly as an instrument if supported).
- **Latency**
  - The plugin is designed to generate patterns ahead-of-time (not sample-accurate
    live input processing), so latency is effectively zero for playback.
- **State saving**
  - The plugin should serialize its parameters (genre, mood, seed, etc.) as part
    of the host’s preset/session state, so reopening a project restores the same
    pattern configuration.

