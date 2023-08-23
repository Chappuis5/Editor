# Editor

## Description
The "Editor" project is a suite of tools designed to facilitate video processing and editing, content analysis, audio transcription, and much more. It is structured around several microlibs, each having a specific functionality.

## Installation
To use "Editor", simply clone the GitHub repository using the following command:
\```bash
git clone https://github.com/Chappuis5/Editor.git
\```

## Microlibs

### Audio
- **audio_transcriber** : Transcribes audio into text.

### Brain
- **brain_gpt** : Uses the GPT model to generate text based on a given input.

### Logger
- **logger** : Provides logging functionalities for the project.

### Scraper
- **video_scraper** : Retrieves videos from various sources.

### Video
- **video_editor** : Provides tools for editing and processing videos.

## Code Conventions

### Function Documentation
Each function should be documented in a clear and concise manner. Here's an example of how functions should be documented:

\```python
def resize_clip(clip, size):
    """
    Resize the frames of a video clip to a given size.
    
    :param clip: The video clip to resize.
    :type clip: moviepy.video.io.ImageSequenceClip.ImageSequenceClip
    :param size: The desired size for the frames.
    :type size: tuple
    :return: Resized video clip.
    :rtype: moviepy.video.io.ImageSequenceClip.ImageSequenceClip
    """
    ...
\```

### Tests
Each microlib should have associated tests to ensure its proper functioning. Tests should be placed in the `tests` folder corresponding to each microlib.

## Contribution
If you wish to contribute to the project, please follow the code conventions mentioned above and submit a pull request for review.

## License
Please refer to the `LICENSE` file for more information on the project's license.
