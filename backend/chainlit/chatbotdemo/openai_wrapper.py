import json
import os
from enum import Enum
import datetime
from typing import Dict, Optional
from textwrap import dedent

import openai
import config
from dotenv import load_dotenv
from rich import print as printr

PRINT_COLOR_USER = "green"


def clean_to_raw_answer(input: str) -> str:
    text = input.strip()
    text = text.replace(".", "")
    text = text.replace('"', '')
    text = text.replace("'", "")
    return text


class Happiness(str, Enum):
    HAPPY = "happy",
    NEUTRAL = "neutral",
    UNHAPPY = "unhappy"


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class Choice:
    def __init__(self, finish_reason: str, index: int, message: Message):
        self.finish_reason = finish_reason
        self.index = index
        self.message = message


class ConsentResponse:
    def __init__(self, consent: bool):
        self.consent: bool = consent


class QuestionWithOptions:
    def __init__(self, question: str, options: list[str]) -> None:
        self.question_text = question
        self.options = options


class PersonInformation:
    def __init__(self, name: str):
        self.name = name
        self.location_country = "Switzerland"


class OpenAi:
    MODEL = "gpt-3.5-turbo"
    LANGUAGE = "English"
    MAX_SENTENCES_SUMMARY = 6
    MAX_REPEATS = 5
    cfg: config.Config = config.Config()

    def __init__(self) -> None:
        load_dotenv()
        key_value = os.environ.get("openai.api_key")
        openai.api_key = key_value

    def request_openai(self, prompt: str, system_hint: Optional[str] = None) -> Dict:
        messages = [{"role": "user", "content": prompt}]
        if system_hint:
            messages.append({"role": "system", "content": system_hint})
        return openai.ChatCompletion.create(model=self.MODEL, messages=messages)

    def transcribe(self, mp3_path) -> str:
        audio_file = open(mp3_path, "rb")

        response = openai.Audio.transcribe("whisper-1", audio_file)
        raw_text = response["text"]  # type: ignore
        text = raw_text.strip()
        printr(f"[{PRINT_COLOR_USER}]User (transcribed): `{text}`")

        return text

    def create_greeting(self, person_information: PersonInformation) -> str:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        prompt = dedent(f"""
		Your are a person working at the customer support.
		The company's name is 'Pilatus Aircraft Ltd.'.
		Your task is to greet the calling customer.
		The customer's name is {person_information.name} and calls from {person_information.location_country}.
		Do not aks for the name.
		The current time is {current_time} h.
		Close by asking how you can help.
		Answer in {self.LANGUAGE}.
		Answer only with the greeting and use the name and location.
		""")

        response = self.request_openai(prompt)
        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        greeting = message.content.strip()
        return greeting

    def create_ending(self, person_information: PersonInformation, successful_call: bool) -> str:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        not_happy_text = "" if successful_call else " not "

        prompt = f"Your are a person working at customer support. \
		The company's name is 'Pilatus'. \
		Your are at the end of the conversation. \
		The customer has {not_happy_text} been satisfied with the services in the call. \
		Your task is to create the ending text. \
		The customer's name is {person_information.name}. \
		The current time is {current_time} h. \
		Answer in {self.LANGUAGE}. \
		Answer only with the ending text."

        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        ending = message.content.strip()

        return ending

    def fake_perform_service(self, customer_name: str, service_name: str) -> str:
        prompt = f"Your are a person working at the customer support. \
		Your task is to create a sentence to confirm the execution of the requested service. \
		The requested service is \"{service_name}\" \
		The customer's name is {customer_name}. \
		Answer in {self.LANGUAGE}. \
		Only respond the confirmation sentence."

        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        greeting = message.content.strip()
        return greeting

    def summarize(self, content: str, source_doc: Optional[str] = None,
                  max_sentences_summary: int = MAX_SENTENCES_SUMMARY) -> str:
        prompt = f"Your are a person working at the customer support. \
		Summarize the following in max {max_sentences_summary} sentences and mention that the source is the `{source_doc}` document: {content}"

        response = self.request_openai(prompt)
        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        answer = message.content.strip()
        return answer

    def check_for_consent(self, statement_to_interpret: str) -> bool:
        prompt = f"Interpret a statement whether it is a consent or not. \
			The statement is in {self.LANGUAGE}. \
			Render your answer only in JSON format. \
			The JSON should only contain a key 'consent' with a boolean value. \
			START OF STATEMENT TO INTERPRET \
			{statement_to_interpret} \
			END OF STATEMENT TO INTERPRET"

        repeats = 0
        while repeats < self.MAX_REPEATS:
            try:
                response = self.request_openai(prompt)
                choice: Choice = response["choices"][0]  # type: ignore
                message = choice.message
                json_content = message.content.strip()
                resp = json.loads(json_content)
                consent = resp["consent"]
                return consent
            except:
                repeats += 1
        return True

    def check_for_anything_to_do(self, statement_to_interpret: str) -> bool:
        prompt = f"In the context of a support request the customer has been asked \
			if there is anything else. \
			Interpret the following answer whether something is to do or not. \
			The statement is in {self.LANGUAGE}. \
			Give the answer only in JSON format. \
			The JSON should only contain a key 'anythingToDo' with a boolean value. \
			START OF STATEMENT TO INTERPRET \
			{statement_to_interpret} \
			END OF STATEMENT TO INTERPRET"

        response = self.request_openai(prompt)
        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        json_content = message.content
        resp = json.loads(json_content)
        consent = resp["anythingToDo"]
        return consent

    def check_for_yes_or_no(self, statement_to_interpret: str) -> bool:
        prompt = f"In the context of a support request the customer has been asked \
			if she wants a confirmation email with a summary. \
			Interpret the following answer whether the customer wants an email or not. \
			The statement is in {self.LANGUAGE}. \
			Give the answer only in JSON format. \
			The JSON should only contain a key 'wantEmailConfirmation' with a boolean value. \
			START OF STATEMENT TO INTERPRET \
			{statement_to_interpret} \
			END OF STATEMENT TO INTERPRET"

        repeats = 0
        while repeats < self.MAX_REPEATS:
            try:
                response = self.request_openai(prompt)
                choice: Choice = response["choices"][0]  # type: ignore
                message = choice.message
                json_content = message.content
                resp = json.loads(json_content)
                consent = resp["wantEmailConfirmation"]
                return consent
            except:
                repeats += 1
        return True

    def check_for_happiness(self, statement: str) -> Happiness:
        prompt = f'Answer with the word "happy", "neutral" or "unhappy" \
			depending on the mood in the text is rather "happy", "neutral" or "unhappy" \
			START OF TEXT \
			{statement} \
			END OF TEXT'

        response = self.request_openai(prompt)
        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        mood_candidate = message.content
        mood_candidate = clean_to_raw_answer(mood_candidate)
        mood = Happiness[mood_candidate.upper()]
        return mood

    def define_question_w_options(self, choices: list[str]) -> QuestionWithOptions:
        json_choices = json.dumps(choices)

        prompt = f"The context is the middle of a conversation with a person. \
		Based on the following array with options defined in JSON format \
		the person has to pick one option: \
		JSON START \
		{json_choices} \
		JSON END \
		Answer only with the question to the person and with no other sentences. \
		Include all options in your answer."

        response = self.request_openai(prompt)
        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        question_with_options = message.content.strip()
        options_question = QuestionWithOptions(question_with_options, choices)
        return options_question

    def get_selected_option(
        self,
        answer_text: str,
        options: list[str]
    ) -> str:
        json_options = json.dumps(options)

        prompt = f"Based on the following array with options defined in JSON format \
		a question was asked to select one option: \
		JSON START \
		{json_options} \
		JSON END \
		The answer to the question was: \"{answer_text}\" \
		Your task is to find a matching option. \
		Your response must only be in JSON format. \
		The JSON format must only contain a key 'selected_option' with a string value of the option. \
		If you could not find a match 'selected_option' is \"NONE\" "

        response = self.request_openai(prompt)
        choice: Choice = response["choices"][0]  # type: ignore
        message = choice.message
        json_content = message.content.strip()
        resp = json.loads(json_content)
        selected_option = resp["selected_option"]
        return selected_option

    def create_german_summary(self) -> None:
        print("Creating a summary in German...")
        with open(self.cfg.get_protocol_path(), 'r') as f:
            protocol_text = f.read()
            prompt = f"Your task is to write a summary from a protocol. \
			Write the summary in German. \
			PROTOCOL START \
			{protocol_text} \
			PROTOCOL END "

            # response = self.request_openai(prompt, "You are a helpful assistant.")
            response = openai.ChatCompletion.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )

            choice: Choice = response["choices"][0]  # type: ignore
            message = choice.message
            german_summary = message.content.strip()
            with open(self.cfg.get_german_summary_path(), 'w') as summary_file:
                summary_file.write(german_summary)
                print(f"Create a summary of the protocol in German written to: {self.cfg.get_german_summary_path()}")


def main() -> None:
    open_ai = OpenAi()
    open_ai.create_german_summary()
    print("Done.")


if __name__ == "__main__":
    main()
