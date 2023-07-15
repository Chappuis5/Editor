import openai
import nltk
from AutoEditor.audio_builder.audio_transcriber import Audio


class GPTBrain:
    def __init__(self, open_ai_key, logger):
        """
        Initialize GPTBrain instance.

        :param open_ai_key: str, OpenAI API key.
        :param logger: logger instance, used for logging information and progress.
        """
        nltk.download('punkt')
        openai.api_key = open_ai_key
        self.logger = logger

    def _read_script(self, script_path):
        """
        Read script from provided file path.

        :param script_path: str, path to the script file.
        :return: str, content of the script file.
        """
        with open(script_path, "r") as script_file:
            return script_file.read()

    def transcribe_audio(self, audio_path):
        """
        Transcribe audio from the provided audio file path.

        :param audio_path: str, path to the audio file.
        :return: list of dict, transcriptions with format [{"start_time": float, "end_time": float, "transcription": str}, ...]
        """
        self.logger.info('Starting audio transcription, please wait...')
        audio_reader = Audio(audio_path)
        audio_reader.convert_m4a_to_mp3()
        audio_reader.transcribe()
        self.logger.info('Audio transcription completed.')
        return audio_reader.get_transcriptions

    def split_text_into_parts(self, text, max_tokens_per_part):
        """
        Split text into parts based on the token limit.

        :param text: str, text to be split.
        :param max_tokens_per_part: int, maximum number of tokens in each part.
        :return: list of str, parts of the text.
        """
        sentences = nltk.sent_tokenize(text)
        parts = []
        current_part = ""
        for sentence in sentences:
            if len((current_part + " " + sentence).split()) <= max_tokens_per_part:
                current_part += " " + sentence
            else:
                parts.append(current_part.strip())
                current_part = sentence
        if current_part.strip():
            parts.append(current_part.strip())
        return parts

    def generate_keywords_for_part(self, part):
        """
        Generate keywords for a part of the text.

        :param part: str, part of the text.
        :return: list of str, keywords generated for the part.
        """
        sentences = nltk.sent_tokenize(part)
        keywords = []
        for sentence in sentences:
            if len(sentence.split()) <= 4096:
                prompt = f"Résumez le texte suivant en un ensemble de mots-clés: {sentence}"
                response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.5, max_tokens=200)
                sentence_keywords = response.choices[0].text.strip().split(',')
                for keyword in sentence_keywords[:2]:
                    keywords.append(keyword)
                    if len(keywords) == 3:
                        break
            if len(keywords) == 3:
                break
        return keywords

    def calculate_parts_keywords_and_times(self, script_path, audio_path):
        """
        Calculate parts, keywords, and times for a script and an audio file.

        :param script_path: str, path to the script file.
        :param audio_path: str, path to the audio file.
        :return: list of dict, information about parts, keywords, and times with format 
                 [{"part": str, "keywords": [str, str, ...], "start_time": float, "end_time": float}, ...]
        """
        video_script = self._read_script(script_path)
        transcriptions = self.transcribe_audio(audio_path)
        total_duration = sum(transcription["end_time"] - transcription["start_time"] for transcription in transcriptions)
        average_reading_speed = len(video_script.split()) / total_duration
        max_words_per_part = int(average_reading_speed * 20)
        parts = self.split_text_into_parts(video_script, max_words_per_part)
        parts_keywords_times = []
        total_parts = len(parts)
        start_time = 0
        for i, part in enumerate(parts):
            keywords = self.generate_keywords_for_part(part)
            end_time = start_time + len(part.split()) / average_reading_speed
            part_dict = {"part": part, "keywords": keywords, "start_time": start_time, "end_time": end_time}
            parts_keywords_times.append(part_dict)
            start_time = end_time
        return parts_keywords_times

