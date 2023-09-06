import os
import pytest
from Audio.audio_transcriber.audio_subtitle import Subtitle, SubtitleOptions
from pytube import YouTube
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

# Mock transcriptions for testing
transcriptions_mock = [
    {'word': 'Hello', 'start_time': 0.0, 'end_time': 0.5},
    {'word': 'world', 'start_time': 0.6, 'end_time': 1.0},
    {'word': '.', 'start_time': 1.1, 'end_time': 1.5},
]

@pytest.fixture
def subtitle_obj():
    return Subtitle(transcriptions=transcriptions_mock)


@pytest.fixture
def subtitle_options():
    return SubtitleOptions(font="Times New Roman", size=18, color="yellow", position="top")


def test_to_srt(subtitle_obj):
    srt_output = subtitle_obj.to_srt()
    expected_output = """1
00:00:00,000 --> 00:00:01,500
Hello world .
"""
    assert srt_output == expected_output  # Checking if words are correctly transcribed to srt format


def test_subtitle_options(subtitle_options):
    assert subtitle_options.font == "Times New Roman"
    assert subtitle_options.size == 18
    assert subtitle_options.color == "yellow"
    assert subtitle_options.position == "top"

    # Test modifying options
    subtitle_options.font = "Arial"
    assert subtitle_options.font == "Arial"


def test_save_to_file(subtitle_obj):
    file_name = "test_output.srt"
    subtitle_obj.save_to_file(file_name)
    assert os.path.exists(file_name)
    with open(file_name, 'r') as f:
        saved_output = f.read()

        expected_output = """1
00:00:00,000 --> 00:00:01,500
Hello world .
"""
    assert saved_output == expected_output

    os.remove(file_name)

def resize_clip_generator(clip, size):
    for frame in clip.iter_frames():
        yield np.array(Image.fromarray(frame).resize(size, Image.LANCZOS))

@pytest.fixture
def video_path():
    # Download the video
    yt = YouTube('https://youtu.be/NcBjx_eyvxc')
    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").asc().first()
    downloaded_path = video_stream.download()

    # Reduce the video quality
    with VideoFileClip(downloaded_path) as video:
        resized_frames = list(resize_clip_generator(video, (
        144, 256)))  # Replace 256 with the actual width corresponding to a height of 144
        low_quality_video = ImageSequenceClip(resized_frames, fps=video.fps)
        low_quality_path = "low_quality_video.mp4"
        low_quality_video.write_videofile(low_quality_path, codec='libx264')
    os.remove(downloaded_path)
    return low_quality_path


def test_burn_to_video(subtitle_obj, video_path):
    # Path to save the video with burned-in subtitles
    output_video_path = "output_video_with_subtitles.mp4"

    # Call the method to burn the subtitles into the video
    subtitle_obj.burn_to_video(video_path, output_video_path)

    # Check if the output video file exists
    assert os.path.exists(output_video_path)

    # Load the output video for additional checks (optional)
    output_video = VideoFileClip(output_video_path)

    # Here, you can add additional checks, for example:
    # - Check the duration of the video
    # - Check the codec, etc.

    # Remove the video files for cleanup
    os.remove(output_video_path)
    os.remove(video_path)
