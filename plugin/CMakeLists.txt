cmake_minimum_required(VERSION 3.15)

project(MidiDrumGeneratorPlugin VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT DEFINED JUCE_DIR)
  message(FATAL_ERROR "JUCE_DIR must be set to your JUCE checkout (where JUCEConfig.cmake lives).")
endif()

list(APPEND CMAKE_MODULE_PATH "${JUCE_DIR}/extras/Build/CMake")
find_package(JUCE CONFIG REQUIRED)

juce_add_plugin(MidiDrumGenerator
  COMPANY_NAME "YourCompany"
  BUNDLE_ID    "com.yourcompany.mididrumgenerator"
  IS_SYNTH     TRUE
  NEEDS_MIDI_INPUT  FALSE
  NEEDS_MIDI_OUTPUT TRUE
  IS_MIDI_EFFECT    TRUE
  COPY_PLUGIN_AFTER_BUILD TRUE
  PLUGIN_MANUFACTURER_CODE MdDG
  PLUGIN_CODE MdDG
  FORMATS VST3 AU
  PRODUCT_NAME "MIDI Drum Generator"
)

target_sources(MidiDrumGenerator
  PRIVATE
    src/PluginProcessor.cpp
    src/PluginEditor.cpp
)

target_compile_definitions(MidiDrumGenerator
  PRIVATE
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
)

target_link_libraries(MidiDrumGenerator
  PRIVATE
    juce::juce_audio_utils
)

