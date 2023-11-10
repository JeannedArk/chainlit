import threading
import asyncio

import chainlit as cl
import azure_lang_service
import ai_communication
import openai_wrapper as openaiw


PRINT_COLOR = "blue"
NO_OPTION_SELECTED = "NONE"
CONDUCTOR_NAME = "AI Assistant"

communication = ai_communication.HumanCommunication()
openai = openaiw.OpenAi()


def printi(msg: str):
    print(f"[{PRINT_COLOR}]{CONDUCTOR_NAME}: {msg}")


async def prompt_message(message: str):
    await cl.Message(content=message).send()
    communication.speak_to_human_async(message)


@cl.on_chat_start
async def chainlit_on_start():
    """
    This function will be called when the chat starts
    """
    printi("Starting chat...")
    await prompt_message("Hallo, ich bin der KI Assistent für Bankenauflagen und Compliance-Richtlinien. Wie kann ich Ihnen helfen?")


@cl.on_message
async def chainlit_on_message(message: cl.Message):
    """
    This function will be called every time a user inputs a message in the UI
    """
    await answer_technical_question(message.content)


async def answer_technical_question(chat_input: str) -> None:
    asking_for_questions = True
    while asking_for_questions:
        # tech_question = self.communication.listen_to_human()

        # self.communication.speak_to_human("Give me a second to look that up.")
        printi("Requesting Azure language service...")
        azure_search_resp = azure_lang_service.search(chat_input)
        if len(azure_search_resp.answers):
            printi("Requesting OpenAI to summarize response...")
            azure_search_answer = azure_search_resp.answers[0]
            answer_summarized = openai.summarize(azure_search_answer.answer, azure_search_answer.source)
            await prompt_message(answer_summarized)
            printi(f"Answer: `{answer_summarized}`")
            printi("Question answered to human.")
            asking_for_questions = False
        else:
            printi("Something went wrong. No answer was found. Will try again...")
            await prompt_message("Entschuldigung, ich konnte keine Antwort finden.")
