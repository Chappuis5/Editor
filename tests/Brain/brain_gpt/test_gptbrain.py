import pytest
from Brain.brain_gpt.gptbrain import *
from unittest.mock import patch, Mock
import nltk
nltk.download('punkt', quiet=True)


# Vous pouvez définir des données de test globales pour réutiliser dans plusieurs tests.
SAMPLE_TEXT = "My name is ChatGPT. How can I help you today?"

def test_split_text_gpt():
    result = split_text_gpt(SAMPLE_TEXT, 5)
    expected = ["My name is ChatGPT.", "How can I help you today?"]
    assert result == expected



# Ici, nous pourrions également simuler d'autres comportements, tels que la lecture d'un fichier ou les appels à d'autres fonctions.

@patch("Brain.brain_gpt.gptbrain.nltk")
@patch("Brain.brain_gpt.gptbrain.openai")
@patch("Brain.brain_gpt.gptbrain.Audio")
def test_helper(mock_audio, mock_open, mock_nltk):
    # Simuler le comportement de nltk.download
    mock_nltk.download.return_value = None

    # Simuler le comportement de open
    mock_open.return_value.__enter__.return_value.read.return_value = SAMPLE_TEXT

    # Simuler le comportement de Audio
    mock_audio_instance = Mock()
    mock_audio_instance.get_transcriptions = [{"word": "Hello", "start_time": 0, "end_time": 1, "pause_after": 0.5}]
    mock_audio.return_value = mock_audio_instance

    options = {"script_path": "D:\\programmation\\Editor\\tests\\script.txt", "audio_path": "dummy_audio_path"}
    mock_logger = Mock()
    open_ai_key = "dummy_key"

    result = Helper(options, mock_logger, open_ai_key)
    # Vous devez définir ce à quoi vous vous attendez pour le résultat ici.
    expected = [Ellipsis]
    assert result == expected