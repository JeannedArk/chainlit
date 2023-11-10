import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

DEBUG = False


def debug_print(*args, **kwargs):
    print(*args, **kwargs) if DEBUG else None


class SoundPlayer:
    def __init__(self):
        pygame.init()

    def play_sound_async(self, file_path: str) -> None:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def play_sound(self, file_path: str) -> None:
        debug_print("Playing sound...")
        self.play_sound_async(file_path)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # 10 milliseconds
