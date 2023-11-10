import threading
from datetime import datetime

import config
import polly_synthesizer
import sound_player
import mp3_recorder
import openai_wrapper as openaiw


class HumanCommunication:
    cfg = config.Config()

    def __init__(self) -> None:
        with open(self.cfg.get_protocol_path(), 'w') as f:
            f.write("Start of the protocol.\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M h')}\n\n")
        self.synthesizer = polly_synthesizer.PollySynthesizer()
        self.player = sound_player.SoundPlayer()
        self.mp3_recorder = mp3_recorder.Mp3Recorder()
        self.openAi = openaiw.OpenAi()

    def speak_to_human(self, text: str) -> None:
        file_path = self.synthesizer.synthesize(text)
        self.player.play_sound(file_path)
        with open(self.cfg.get_protocol_path(), 'a') as f:
            f.write(f"SUPPORT: {text}\n\n")

    def speak_to_human_async(self, text: str) -> None:
        def speak():
            self.speak_to_human(text)

        thread_one = threading.Thread(target=speak)
        thread_one.start()

    def listen_to_human(self) -> str:
        user_response_mp3_file_path = self.mp3_recorder.record_mp3()
        user_response_text = self.openAi.transcribe(user_response_mp3_file_path)
        with open(self.cfg.get_protocol_path(), 'a') as f:
            f.write(f"CUSTOMER: {user_response_text}\n\n")
        return user_response_text

    def mark_ending(self, openai: openaiw.OpenAi) -> None:
        with open(self.cfg.get_protocol_path(), 'a') as f:
            f.write("End of the protocol.\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M h')}\n\n")
        openai.create_german_summary()
