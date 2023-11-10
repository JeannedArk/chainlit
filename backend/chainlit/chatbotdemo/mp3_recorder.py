import wave
import threading
import os
from tempfile import gettempdir

import pydub  # For converting wav to mp3
import pyaudio  # For Audio recording
from rich.console import Console

DEBUG = False


def debug_print(*args, **kwargs):
    print(*args, **kwargs) if DEBUG else None


class KeepRecordingState:
    def __init__(self):
        self.keep_recording = True


class Mp3Recorder:
    CHUNK_SIZE = 1024  # Record in chunks of 1024 bytes
    MONO_CHANNEL = 1  # Only mono
    SAMPLES_PER_SECOND = 44100  # Record at 44100 samples per second

    def record_mp3(self) -> str:
        channels = 1  # Only mono

        wav_filepath = os.path.join(gettempdir(), "recording.wav")
        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        stream = p.open(format=pyaudio.paInt16,
                        channels=self.MONO_CHANNEL,
                        rate=self.SAMPLES_PER_SECOND,
                        frames_per_buffer=self.CHUNK_SIZE,
                        input=True)

        console = Console()
        with console.status("Starting to listen (Hit Enter to stop)...") as status:
            keep_recording_state = KeepRecordingState()

            def wait_for_enter():
                input()
                keep_recording_state.keep_recording = False

            threading.Thread(target=wait_for_enter).start()

            frames: list[bytes] = []
            while keep_recording_state.keep_recording:
                data = stream.read(self.CHUNK_SIZE)
                frames.append(data)

            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            p.terminate()

        debug_print('Listening stopped.')

        # Save the recorded data as a WAV file
        with wave.open(wav_filepath, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.SAMPLES_PER_SECOND)
            wf.writeframes(b''.join(frames))

        mp3_filepath = self._convert_wav_to_mp3(wav_filepath)
        return mp3_filepath

    def _convert_wav_to_mp3(self, wav_filepath: str) -> str:
        mp3_filepath = os.path.join(gettempdir(), "recording.mp3")
        sound = pydub.AudioSegment.from_wav(wav_filepath)
        sound.export(mp3_filepath, format="mp3")
        return mp3_filepath


def main() -> None:
    recorder = Mp3Recorder()
    recorder.record_mp3()


if __name__ == '__main__':
    main()
