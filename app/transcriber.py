import speech_recognition as sr
from moviepy.editor import VideoFileClip  # For MP4 to audio extraction


class Transcriber:
    def __init__(self, model_path=None):
        """
        Initializes the SpeechRecognizer with an optional language model path.

        Args:
            model_path (str, optional): Path to the language model file. Defaults to None.
        """
        self.recognizer = sr.Recognizer()
        self.language_code = "es-ES"
        self.model = None

        if model_path:
            self.model = sr.AudioFile(model_path)  # Load the language model

    def extract_audio(self, mp4_file):
        """
        Extracts audio from the provided MP4 file and saves it as a WAV file.

        Args:
            mp4_file (str): Path to the MP4 file.

        Returns:
            str: Path to the extracted audio file (WAV), or None on error.
        """
        try:
            clip = VideoFileClip(mp4_file)
            audio_clip = clip.audio
            audio_path = "extracted_audio.wav"
            audio_clip.write_audiofile(audio_path)
            return audio_path
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return None

    def transcribe(self, mp4_file):
        """
        Transcribes audio from the provided MP4 file using chosen language settings.

        Args:
            mp4_file (str): Path to the MP4 file.

        Returns:
            str: The transcribed text, or None on error.
        """
        audio_file = self.extract_audio(mp4_file)
        if not audio_file:
            return None

        with sr.AudioFile(audio_file) as source:
            recorded_audio = self.recognizer.record(source)

        if self.model:
            try:
                text = self.recognizer.recognize_lm(self.model, recorded_audio)  # Use language model
                return text
            except sr.UnknownValueError:
                print("Audio could not be understood using the language model.")
        else:
            try:
                text = self.recognizer.recognize_google(recorded_audio, language=self.language_code)
                return text
            except sr.UnknownValueError:
                print("Audio could not be understood using online recognition.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

        return None 