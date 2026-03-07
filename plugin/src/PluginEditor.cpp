#include "PluginEditor.h"
#include "PluginProcessor.h"

MidiDrumGeneratorAudioProcessorEditor::MidiDrumGeneratorAudioProcessorEditor(MidiDrumGeneratorAudioProcessor& p)
    : juce::AudioProcessorEditor(&p),
      processor(p)
{
    setSize(360, 160);

    complexitySlider.setSliderStyle(juce::Slider::LinearHorizontal);
    complexitySlider.setTextBoxStyle(juce::Slider::TextBoxRight, false, 60, 20);
    addAndMakeVisible(complexitySlider);

    swingSlider.setSliderStyle(juce::Slider::LinearHorizontal);
    swingSlider.setTextBoxStyle(juce::Slider::TextBoxRight, false, 60, 20);
    addAndMakeVisible(swingSlider);

    auto& params = processor.getValueTreeState();
    complexityAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(params, "complexity", complexitySlider);
    swingAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(params, "swing", swingSlider);
}

void MidiDrumGeneratorAudioProcessorEditor::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::black);
    g.setColour(juce::Colours::white);
    g.setFont(18.0f);
    g.drawFittedText("MIDI Drum Generator", getLocalBounds().removeFromTop(30), juce::Justification::centred, 1);

    g.setFont(14.0f);
    g.drawText("Complexity", 10, 50, 120, 20, juce::Justification::left);
    g.drawText("Swing", 10, 90, 120, 20, juce::Justification::left);
}

void MidiDrumGeneratorAudioProcessorEditor::resized()
{
    complexitySlider.setBounds(130, 50, getWidth() - 140, 20);
    swingSlider.setBounds(130, 90, getWidth() - 140, 20);
}

