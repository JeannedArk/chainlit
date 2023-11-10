from contextlib import closing
import os
from tempfile import gettempdir

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError

DEBUG = False


def debug_print(*args, **kwargs):
    print(*args, **kwargs) if DEBUG else None


class PollySynthesizer:

    def __init__(self):
        self.session = Session()
        self.polly = self.session.client("polly")

    def synthesize(self, text: str) -> str:
        debug_print("Requesting Amazon Polly...")
        try:
            # Request speech synthesis
            # https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat="mp3",
                # VoiceId="Ruth",
                VoiceId="Vicki",
                Engine="neural",
                # Engine="standard",
                LanguageCode="de-DE",
            )
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            raise error

        # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output_filepath = os.path.join(gettempdir(), "polly_synthesized.mp3")
                try:  # Open a file for writing the output as a binary stream
                    with open(output_filepath, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    raise error
            return output_filepath
        else:
            # The response didn't contain audio data, exit gracefully
            error_message = "Could not stream audio"
            print(error_message)
            raise Exception(error_message)
