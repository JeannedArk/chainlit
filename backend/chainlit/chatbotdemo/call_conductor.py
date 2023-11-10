from rich import print

import ai_communication
import ai_text_analyzer
import openai_wrapper as openaiw
import azure_lang_service

PRINT_COLOR = "blue"
NO_OPTION_SELECTED = "NONE"
CONDUCTOR_NAME = "AI Assistant"


class ServiceCallConductor:

    def __init__(self, service_options: list[str]) -> None:
        self.service_options = service_options
        self.communication = ai_communication.HumanCommunication()
        self.analyzer = ai_text_analyzer.TextAnalyzer()
        self.openai = openaiw.OpenAi()
        self.abrupt_end_of_service = False
        self.successful_service_call = False

    def printi(self, msg: str):
        print(f"[{PRINT_COLOR}]{CONDUCTOR_NAME}: {msg}")

    def greet(self, person_information: openaiw.PersonInformation) -> None:
        self.printi("Will greet the calling customer...")
        greeting = self.openai.create_greeting(person_information)
        self.communication.speak_to_human(greeting)
        greeting_answer = self.communication.listen_to_human()
        self.selected_option = self.openai.get_selected_option(greeting_answer, self.service_options)
        self.printi("Greeting finished.")

    def has_selected_option(self) -> bool:
        return self.selected_option != NO_OPTION_SELECTED

    def get_selected_option(self) -> str:
        return self.selected_option

    def present_options_and_ask_to_choose(self) -> None:
        self.printi("Presenting all the service options...")
        self.communication.speak_to_human("I can help you with several services.")
        choose_option_text = self.openai.define_question_w_options(self.service_options)
        self.communication.speak_to_human(choose_option_text.question_text)
        human_answer = self.communication.listen_to_human()
        self.selected_option = self.openai.get_selected_option(human_answer, self.service_options)
        self.printi("Customer answered to presented service options.")

    def communicate_abrupt_end_of_service(self) -> None:
        self.printi("The conversation stopped unexpectedly.")
        self.communication.speak_to_human("There is nothing more I can help you with. Have a nice day! Bye bye!")
        self.abrupt_end_of_service = True
        self.communication.mark_ending(self.openai)

    def ask_for_additional_services(self) -> None:
        self.printi("Asking for anything else to do...")
        self.communication.speak_to_human("Is there anything else I can help you with?")
        anything_else_answer = self.communication.listen_to_human()
        # Check if human already made a valid choice
        current_selected_option = self.openai.get_selected_option(anything_else_answer, self.service_options)
        if current_selected_option != NO_OPTION_SELECTED:
            self.printi("Customer chose another service option.")
            self.selected_option = current_selected_option
        else:
            human_wants_more = self.analyzer.text_has_consent(anything_else_answer)
            if human_wants_more:
                self.printi("Customer wants another service option.")
                self.present_options_and_ask_to_choose()
            else:
                self.printi("Customer doesn't want anything else.")
                self.communication.speak_to_human("No worries.")
                self.selected_option = NO_OPTION_SELECTED

    def ask_for_email_services(self) -> None:
        self.printi("Asking to send the protocol per mail...")
        self.communication.speak_to_human(
            "Would you like to have the answer and a summary of our conversation per mail?")
        anything_else_answer = self.communication.listen_to_human()
        send_mail = self.openai.check_for_yes_or_no(anything_else_answer)
        if send_mail:
            self.printi("Customer wants an email.")
            self.communication.speak_to_human(
                "Thank you. We will send you a mail with the answer and a summary of our conversation.")
        else:
            self.printi("Customer doesn't want an email.")
            self.communication.speak_to_human("Thank you. We won't send you an email.")
        self.selected_option = NO_OPTION_SELECTED

    def fake_perform_service(
        self,
        person_information: openaiw.PersonInformation,
    ) -> None:
        self.printi("Confirming service execution...")
        confirmation_text = self.openai.fake_perform_service(
            person_information.name,
            self.selected_option
        )
        self.communication.speak_to_human(confirmation_text)
        self.printi("Execution confirmed to human.")

    def answer_technical_question(
        self,
        person_information: openaiw.PersonInformation,
    ) -> None:
        asking_for_questions = True
        while asking_for_questions:
            self.communication.speak_to_human("What's your technical question?")
            tech_question = self.communication.listen_to_human()

            self.communication.speak_to_human("Give me a second to look that up.")
            self.printi("Requesting Azure language service...")
            azure_search_resp = azure_lang_service.search(tech_question)
            if len(azure_search_resp.answers):
                self.printi("Requesting OpenAI to summarize response...")
                azure_search_answer = azure_search_resp.answers[0]
                answer_summarized = self.openai.summarize(azure_search_answer.answer, azure_search_answer.source)
                self.communication.speak_to_human(f"Your answer is: {answer_summarized}")
                self.printi(f"Answer: `{answer_summarized}`")
                self.printi("Question answered to human.")
                asking_for_questions = False
            else:
                self.printi("Something went wrong. No answer was found. Will try again...")
                self.communication.speak_to_human("Sorry, no answer could be found.")

    def ask_for_final_feedback_and_finish(
        self,
        person_information: openaiw.PersonInformation
    ) -> None:
        self.printi("Asking human for final feedback...")
        self.communication.speak_to_human("We are at the end of our conversation.")
        self.communication.speak_to_human("Have you been satisfied with the services?")
        satisfied_answer = self.communication.listen_to_human()
        self.printi("Feedback received.")
        happy = self.analyzer.text_is_happy(satisfied_answer)
        if happy:
            self.printi("Customer is happy")
            self.successful_service_call = True
        else:
            unhappy = self.analyzer.text_is_unhappy(satisfied_answer)
            if unhappy:
                self.printi("Customer is unhappy")
                self.successful_service_call = False
            else:
                satisfied_consent = self.analyzer.text_has_consent(satisfied_answer)
                if satisfied_consent:
                    self.printi("Customer consents with satisfaction statement.")
                else:
                    self.printi("Customer does not consent with satisfaction statement.")
                self.successful_service_call = satisfied_consent
        ending_text = self.openai.create_ending(person_information, self.successful_service_call)
        self.printi("Ending conversation...")
        self.communication.speak_to_human(ending_text)
        self.printi("Conversation ended...")
        self.communication.mark_ending(self.openai)
