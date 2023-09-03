import os
from Brain.brain_gpt.gptbrain import *
import nltk
nltk.download('punkt', quiet=True)

current_dir = os.path.dirname(os.path.abspath(__file__))  # This gets the directory of the current script.
project_root = os.path.join(current_dir, '..', '..', '..')  # This will reach the 'Editor' directory.

# Now, construct the paths:
script_path = os.path.join(project_root, 'tests', 'script.txt')
audio_path_m4a = os.path.join(project_root, 'tests', 'audio.m4a')
audio_path_mp3 = os.path.join(project_root, 'tests', 'audio.mp3')

SAMPLE_TEXT = "My name is ChatGPT. How can I help you today?"


def test_split_text_gpt():
    result = split_text_gpt(SAMPLE_TEXT, 5)
    expected = ["My name is ChatGPT.", "How can I help you today?"]
    assert result == expected
