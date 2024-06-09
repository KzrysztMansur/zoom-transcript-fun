import os
import speech_recognition as sr
from pyAudioAnalysis import audioSegmentation as aS
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

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

            
    def diarize_audio(self, audio_file, n_speakers=2):
        segmentation = aS.speaker_diarization(audio_file, n_speakers=n_speakers, plot_res=False)
        labels = segmentation[0]  # Extracting labels array
        segments = []
        start = 0
        current_label = labels[0]  # Initial label
        
        for i, label in enumerate(labels[1:], start=1):
            if label != current_label:
                segments.append((start, i, current_label))
                start = i
                current_label = label


        # Add the last segment
        segments.append((start, len(labels), current_label))
        return segments

    def transcribe(self, mp4_file):
        """
        Transcribes audio from the provided MP4 file using chosen language settings.

        Args:
            mp4_file (str): Path to the MP4 file.

        Returns:
            str: The transcribed text, or None on error.
        """
        if mp4_file.endswith(".mp4"):
            audio_file = self.extract_audio(mp4_file)
        else:
            audio_file = mp4_file
        if not audio_file:
            return None

        segmentation = self.diarize_audio(audio_file)
        
        # Transcribe each segment
        transcriptions = []
        audio = AudioSegment.from_wav(audio_file)
        recognizer = sr.Recognizer()
        unintelligible_count = 0
        
        for start, end, speaker in segmentation:
            segment_audio = audio[start * 1000:end * 1000]
            segment_audio.export("temp_segment.wav", format="wav")
            
            with sr.AudioFile("temp_segment.wav") as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language=self.language_code)
                except sr.UnknownValueError:
                    text = "[Unintelligible]"
                    unintelligible_count += 1
                    if unintelligible_count > 3:
                        break
                except sr.RequestError as e:
                    text = f"[Error: {e}]"
                transcriptions.append((speaker, text))
        
        os.remove("temp_segment.wav")
        return transcriptions

#
# 
# transcriber = Transcriber()
# transcriptions = transcriber.transcribe("app/extracted_audio.wav")
# for i, (speaker, transcription) in enumerate(transcriptions, start=1):
#     print(f"Speaker {speaker}: {transcription}")
