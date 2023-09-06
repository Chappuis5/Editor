import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List, Optional
import cv2
import os

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
font_dir = os.path.join(current_dir, '..', 'fonts')


class SubtitleOptions:
    def __init__(self, font: str = "Arial", size: int = 16, color: str = "white", position: str = "bottom"):
        """
        Initialize the SubtitleOptions object for subtitle customization.

        :param font: Font type for the subtitle.
        :type font: str
        :param size: Font size for the subtitle.
        :type size: int
        :param color: Font color for the subtitle.
        :type color: str
        :param position: Position of the subtitle on screen.
        :type position: str
        """
        self.font = font
        self.size = size
        self.color = color
        self.position = position


class Subtitle:
    def __init__(self, transcriptions: List[dict], options: SubtitleOptions = None):
        """
        Initialize the Subtitle object for generating .srt files.

        :param transcriptions: List of transcriptions with word, start_time, end_time etc.
        :type transcriptions: List[dict]
        :param options: SubtitleOptions object to specify subtitle appearance.
        :type options: SubtitleOptions
        """
        self.transcriptions = transcriptions
        self.options = options if options else SubtitleOptions()

    def to_srt(self, length_limit: Optional[int] = 4, endpoint_sec: float = 0.5) -> str:
        """
        Convert the transcriptions to .srt format.

        :param length_limit: Maximum number of words per subtitle section.
        :type length_limit: Optional[int]
        :param endpoint_sec: Time gap to end a subtitle section and start a new one.
        :type endpoint_sec: float
        :return: Subtitles in .srt format.
        :rtype: str
        """
        def second_to_timecode(x: float) -> str:
            hour, x = divmod(x, 3600)
            minute, x = divmod(x, 60)
            second, x = divmod(x, 1)
            millisecond = int(x * 1000.)
            return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

        def _helper(end: int) -> None:
            lines.append("%d" % section)
            lines.append(
                "%s --> %s" %
                (
                    second_to_timecode(self.transcriptions[start]['start_time']),
                    second_to_timecode(self.transcriptions[end]['end_time'])
                )
            )
            lines.append(' '.join(x['word'] for x in self.transcriptions[start:(end + 1)]))
            lines.append('')

        lines = []
        section = 1
        start = 0
        for k in range(1, len(self.transcriptions)):
            if ((self.transcriptions[k]['start_time'] - self.transcriptions[k - 1]['end_time']) >= endpoint_sec) or \
                    (length_limit is not None and (k - start) >= length_limit):
                _helper(k - 1)
                start = k
                section += 1
        _helper(len(self.transcriptions) - 1)

        return '\n'.join(lines)

    def save_to_file(self, file_name: str):
        """
        Save the generated .srt content into a file.

        :param file_name: The name of the output file.
        :type file_name: str
        """
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(self.to_srt())

    def burn_to_video(self, video_path: str, output_path: str):
        """
        Burn the generated subtitles into a video using OpenCV and PIL for custom fonts.

        :param video_path: The path to the video file.
        :type video_path: str
        :param output_path: The path to save the video with burned-in subtitles.
        :type output_path: str
        """
        # Initialize VideoCapture and VideoWriter
        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

        # Map options
        color_map = {'white': (255, 255, 255), 'black': (0, 0, 0)}
        position_map = {'bottom': (50, int(cap.get(4)) - 50), 'top': (50, 50)}
        # Font mapping
        font_map = {
            'Arial': os.path.join(font_dir, 'arial.ttf'),
            'LemonMilk': os.path.join(font_dir, 'LEMONMILK-Regular.otf')
        }

        font = ImageFont.truetype(font_map[self.options.font], self.options.size)

        for i, transcription in enumerate(self.transcriptions):
            ret, frame = cap.read()
            if not ret:
                break

            start_time = transcription['start_time']
            end_time = transcription['end_time']
            text = transcription['word']

            # Convert frame to PIL Image
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(frame_pil)

            # Draw text on frame
            draw.text(position_map[self.options.position], text, font=font, fill=color_map[self.options.color])

            # Convert PIL Image back to OpenCV format
            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

            # Write the frame
            out.write(frame)

        # Release VideoCapture and VideoWriter
        cap.release()
        out.release()
        cv2.destroyAllWindows()

