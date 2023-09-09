import os
import pytest
from Audio.audio_transcriber.audio_transcriber import Audio


@pytest.fixture
def audio_path():
    # Cela remontera de trois niveaux par rapport au dossier contenant le script de test actuel
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, "audio.mp3")


@pytest.fixture
def audio_m4a_path():
    # Cela remontera de trois niveaux par rapport au dossier contenant le script de test actuel
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, "audio.m4a")


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

def test_reduce_noise_audio(audio_obj):
    audio_obj.reduce_noise_audio(0.5)
    assert os.path.exists(audio_obj.file_path.rsplit('.', 1)[0]+"_denoised.mp3")
