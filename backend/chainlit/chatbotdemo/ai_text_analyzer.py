import polly_synthesizer
import sound_player
import mp3_recorder
import openai_wrapper as openaiw


class TextAnalyzer:

    def __init__(self) -> None:
        self.synthesizer = polly_synthesizer.PollySynthesizer()
        self.player = sound_player.SoundPlayer()
        self.mp3_recorder = mp3_recorder.Mp3Recorder()
        self.openAi = openaiw.OpenAi()

    def text_has_consent(self, text: str) -> bool:
        return self.openAi.check_for_consent(text)

    def text_is_happy(self, text: str) -> bool:
        happiness_result: openaiw.Happiness = self.openAi.check_for_happiness(text)
        is_happy = openaiw.Happiness.HAPPY == happiness_result
        return is_happy

    def text_is_unhappy(self, text: str) -> bool:
        happiness_result: openaiw.Happiness = self.openAi.check_for_happiness(text)
        is_unhappy = openaiw.Happiness.UNHAPPY == happiness_result
        return is_unhappy
