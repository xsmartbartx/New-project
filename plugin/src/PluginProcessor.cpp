#include "PluginProcessor.h"
#include "PluginEditor.h"

MidiDrumGeneratorAudioProcessor::MidiDrumGeneratorAudioProcessor()
    : juce::AudioProcessor(
          BusesProperties().withOutput("Output", juce::AudioChannelSet::stereo(), true)),
      parameters(*this, nullptr, "PARAMS", {
                                             std::make_unique<juce::AudioParameterFloat>("genre", "Genre", 0.0f, 7.0f, 1.0f),
                                             std::make_unique<juce::AudioParameterFloat>("mood", "Mood", 0.0f, 3.0f, 0.0f),
                                             std::make_unique<juce::AudioParameterFloat>("bpm", "BPM", 40.0f, 240.0f, 140.0f),
                                             std::make_unique<juce::AudioParameterFloat>("complexity", "Complexity", 0.0f, 1.0f, 0.5f),
                                             std::make_unique<juce::AudioParameterFloat>("swing", "Swing", 0.0f, 100.0f, 0.0f),
                                         })
{
}

void MidiDrumGeneratorAudioProcessor::prepareToPlay(double /*sampleRate*/, int /*samplesPerBlock*/)
{
}

void MidiDrumGeneratorAudioProcessor::releaseResources()
{
}

bool MidiDrumGeneratorAudioProcessor::isBusesLayoutSupported(const BusesLayout& layouts) const
{
    return layouts.getMainOutputChannelSet() == juce::AudioChannelSet::stereo();
}

void MidiDrumGeneratorAudioProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    buffer.clear();
    generatePatternIfNeeded(getSampleRate(), getBlockSize(), midiMessages);
}

juce::AudioProcessorEditor* MidiDrumGeneratorAudioProcessor::createEditor()
{
    return new MidiDrumGeneratorAudioProcessorEditor(*this);
}

void MidiDrumGeneratorAudioProcessor::getStateInformation(juce::MemoryBlock& destData)
{
    if (auto xml = parameters.copyState().createXml())
    {
        copyXmlToBinary(*xml, destData);
    }
}

void MidiDrumGeneratorAudioProcessor::setStateInformation(const void* data, int sizeInBytes)
{
    if (auto xml = getXmlFromBinary(data, sizeInBytes))
    {
        parameters.replaceState(juce::ValueTree::fromXml(*xml));
    }
}

void MidiDrumGeneratorAudioProcessor::generatePatternIfNeeded(double /*sampleRate*/, int /*samplesPerBlock*/, juce::MidiBuffer& /*midiMessages*/)
{
    // Placeholder: hook for integrating the MIDI pattern generator.
    // For an initial version, this processor can:
    // - Generate a fixed pattern when playback starts, or
    // - Trigger generation via a button in the editor and schedule notes via MidiBuffer.
}

//==============================================================================
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new MidiDrumGeneratorAudioProcessor();
}

