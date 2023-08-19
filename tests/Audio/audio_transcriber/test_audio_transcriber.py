import os
import pytest
from pydub import AudioSegment
from Audio.audio_transcriber.audio_transcriber import Audio

@pytest.fixture
def audio_path():
    return "D:\\programmation\\Editor\\tests\\audio.mp3"

@pytest.fixture
def audio_m4a_path():
    return "D:\\programmation\\Editor\\tests\\audio.m4a"

@pytest.fixture
def audio_obj(audio_path):
    return Audio(audio_path)

def test_convert_to_wav(audio_obj, audio_path):
    audio_obj.convert_to_wav()
    assert audio_obj.file_path.endswith('.wav')
    assert os.path.exists(audio_obj.file_path)

def test_convert_m4a_to_mp3(audio_m4a_path):
    audio_obj = Audio(audio_m4a_path)
    audio_obj.convert_m4a_to_mp3()
    assert audio_obj.file_path.endswith('.mp3')
    assert os.path.exists(audio_obj.file_path)

@pytest.mark.skip("This test requires the pvleopard library and an access key.")
def test_transcribe(audio_obj):
    audio_obj.transcribe()
    assert len(audio_obj.get_transcriptions) > 0
    for transcription in audio_obj.get_transcriptions:
        assert 'word' in transcription
        assert 'start_time' in transcription
        assert 'end_time' in transcription
        assert 'confidence' in transcription
        assert 'pause_after' in transcription
