import chainlit as cl
from rich import print
import openai_wrapper as openaiw
import azure_lang_service
import ai_communication


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
    chat_input = message.content
    printi(f"Azure language service search: {chat_input}")
    azure_search_resp = azure_lang_service.search(chat_input)
    if len(azure_search_resp.answers) or azure_search_resp.answers[0] is None:
        printi("Requesting OpenAI to summarize response...")
        azure_search_answer = azure_search_resp.answers[0]
        # Send intermediate answer
        await cl.Message(
            content=azure_search_answer.answer,
            parent_id=message.id,
        ).send()
        answer_summarized = openai.summarize(azure_search_answer.answer, azure_search_answer.source)
        printi(f"Answer: `{answer_summarized}`")
        await prompt_message(answer_summarized)
    else:
        printi("Something went wrong. No answer was found.")
        await prompt_message("Entschuldigung, ich konnte keine Antwort finden.")


@cl.on_start_recording
async def chainlit_on_start_recording():
    print(f"chainlit_on_start_recording")
    transcribed_human_input = communication.listen_to_human()
    print(f"transcribed_human_input: {transcribed_human_input}")
    await cl.Message(content=transcribed_human_input).send_transcribed_message()


@cl.on_stop_recording
async def chainlit_on_stop_recording():
    print(f"chainlit_on_stop_recording")
