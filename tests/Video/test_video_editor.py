import pytest
from Video.video_editor import VideoEditor
import os
from pytube import YouTube
import requests
from moviepy.editor import VideoFileClip


# Définir les chemins des vidéos et de l'audio à télécharger pour les tests
VIDEO_URLS = [
    'https://youtu.be/NcBjx_eyvxc',
    'https://www.youtube.com/watch?v=kTWoeqPXpuo'
]
AUDIO_URL = 'https://incompetech.com/music/royalty-free/mp3-royaltyfree/Vibing%20Over%20Venus.mp3'

# Créer une instance de VideoEditor pour les tests
editor = VideoEditor()

def download_video_with_pytube(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download(output_path=os.path.dirname(output_path), filename=os.path.basename(output_path))

def download_audio_with_requests(url, output_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download audio from {url}")


@pytest.fixture(scope="module")
def downloaded_videos():
    video_paths = []
    for url in VIDEO_URLS:
        sanitized_name = editor.sanitize_filename(url.split('/')[-1])
        output_path = os.path.join(editor.tmp_dir, f"{sanitized_name}.mp4")
        download_video_with_pytube(url, output_path)

        # Downsample the video for testing
        with VideoFileClip(output_path) as video:
            # Resize the video to half its original dimensions using the resize_clip function from VideoEditor
            resized_video = editor.resize_clip(video, (int(video.size[0] * 0.5), int(video.size[1] * 0.5)))
            resized_output_path = os.path.join(editor.tmp_dir, f"{sanitized_name}_resized.mp4")

            # Write the video with reduced bitrate and no audio
            resized_video.write_videofile(resized_output_path, codec='libx264', bitrate="100k", audio=False)

        video_paths.append(resized_output_path)
    return video_paths


@pytest.fixture(scope="module")
def downloaded_audio():
    output_path = os.path.join(editor.tmp_dir, "audio_test.mp3")
    download_audio_with_requests(AUDIO_URL, output_path)
    return output_path

def test_sanitize_filename():
    assert editor.sanitize_filename("test?:<>*|file.mp4") == "testfile.mp4"
    assert editor.sanitize_filename("a" * 300 + ".mp4") == "a" * 255

def test_trim_video(downloaded_videos):
    trimmed_path = os.path.join(editor.tmp_dir, "trimmed_video.mp4")
    editor.trim_video(downloaded_videos[0], 10, 20, trimmed_path)
    assert os.path.exists(trimmed_path)

def test_concatenate_videos(downloaded_videos):
    concatenated_path = os.path.join(editor.tmp_dir, "concatenated_video.mp4")
    editor.concatenate_videos(downloaded_videos, concatenated_path)
    assert os.path.exists(concatenated_path)

def test_add_audio(downloaded_audio, downloaded_videos):
    video_with_audio_path = editor.add_audio(downloaded_audio, downloaded_videos[0])
    assert os.path.exists(video_with_audio_path)


def test_process_videos(downloaded_audio, downloaded_videos):
    liked_videos_by_part = {
        "part1": [
            {"url": VIDEO_URLS[0], "duration": 10, "part_duration": 20},
            {"url": VIDEO_URLS[1], "duration": 10, "part_duration": 20}
        ]
    }
    final_video_path = None
    try:
        final_video_path = editor.process_videos(liked_videos_by_part, downloaded_audio)
    except Exception as e:
        pytest.fail(f"Error occurred while processing videos: {e}")
    assert final_video_path and os.path.exists(final_video_path)

# Supprimer les vidéos et l'audio téléchargés après les tests
@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    for url in VIDEO_URLS:
        sanitized_name = editor.sanitize_filename(url.split('/')[-1])
        video_path = os.path.join(editor.tmp_dir, f"{sanitized_name}.mp4")
        resized_video_path = os.path.join(editor.tmp_dir, f"{sanitized_name}_resized.mp4")

        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(resized_video_path):
            os.remove(resized_video_path)

    audio_path = os.path.join(editor.tmp_dir, "audio_test.mp3")
    if os.path.exists(audio_path):
        os.remove(audio_path)


