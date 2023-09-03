import os
import pvleopard
from pydub import AudioSegment
import noisereduce as nr
import soundfile as sf

class Audio:
    
    def __init__(self, file_path: str):
        """
        Initialize the Audio object.

        :param file_path: Path to the audio file.
        :type file_path: str
        """
        self.file_path = file_path
        self.transcriptions = []

    def convert_to_wav(self):
        """
        Convert the audio file to WAV format. 
        If it's already in WAV format, nothing is done.
        """
        # Check if the file is already in WAV format
        if self.file_path.lower().endswith('.wav'):
            return

        # Load the MP3 audio file
        audio = AudioSegment.from_file(self.file_path, format='mp3')

        # Change the file extension to WAV
        wav_file_path = self.file_path.rsplit('.', 1)[0] + '.wav'

        # Export the audio in WAV format
        audio.export(wav_file_path, format='wav')

        # Update the file path to the converted WAV file
        self.file_path = wav_file_path

    def convert_m4a_to_mp3(self):
        """
        Convert an m4a audio file to mp3 format. 
        If it's not an m4a file, an informative message is printed.
        """
        # Check if the file is in m4a format
        if not self.file_path.lower().endswith('.m4a'):
            print("File is not in .m4a format")
            return

        # Load the m4a audio file
        audio = AudioSegment.from_file(self.file_path, format='m4a')

        # Change the file extension to mp3
        mp3_file_path = self.file_path.rsplit('.', 1)[0] + '.mp3'

        # Export the audio in mp3 format
        audio.export(mp3_file_path, format='mp3')

        # Update the file path to the converted mp3 file
        self.file_path = mp3_file_path
    
    def reduce_noise_audio(self, prop_decrease:float):
        """
        Reduce noise from an audio file.
        prop_decrease est un paramètre de type float allant de 0.0 à 1.0
        """
        # Lecture du fichier audio
        data, fs = sf.read(self.file_path)

        # Réduire le bruit
        y_denoised = nr.reduce_noise(
            y=data, 
            sr=fs,
            prop_decrease=prop_decrease
        )

        # Sauvegarder l'audio débruité
        sf.write(self.file_path.rsplit('.', 1)[0]+"_denoised.mp3", y_denoised, fs)


    def transcribe(self):
        """
        Transcribe the audio file using the pvleopard library.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "leopard_params_fr.pv")

        leopard = pvleopard.create(access_key="JHRxxr3akK4RilsSIOyULG8IMwwmbMQX6fLcTeB2yXgXSsDWcexbdA==",
                                   model_path=model_path)

        # Process the audio file
        transcript, words = leopard.process_file(self.file_path)

        # Convert the words to transcriptions format
        for i, word in enumerate(words):
            pause_after = words[i + 1].start_sec - word.end_sec if i + 1 < len(words) else 0
            self.transcriptions.append({
                'word': word.word,
                'start_time': word.start_sec,
                'end_time': word.end_sec,
                'confidence': word.confidence,
                'pause_after': pause_after
            })

    @property
    def get_transcriptions(self) -> list:
        """
        Retrieve the transcriptions of the audio.

        :return: List of transcriptions.
        :rtype: list
        """
        return self.transcriptions

