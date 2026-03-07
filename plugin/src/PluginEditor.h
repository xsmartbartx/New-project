#pragma once

#include <JuceHeader.h>

class MidiDrumGeneratorAudioProcessor;

class MidiDrumGeneratorAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:
    explicit MidiDrumGeneratorAudioProcessorEditor(MidiDrumGeneratorAudioProcessor&);
    ~MidiDrumGeneratorAudioProcessorEditor() override = default;

    void paint(juce::Graphics&) override;
    void resized() override;

private:
    MidiDrumGeneratorAudioProcessor& processor;

    juce::Slider complexitySlider;
    juce::Slider swingSlider;

    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> complexityAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> swingAttachment;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MidiDrumGeneratorAudioProcessorEditor)
};

