from openai_wrapper import PersonInformation
from call_conductor import ServiceCallConductor
from rich.console import Console

NO_OPTION_SELECTED = "NONE"

SERVICE_OPT_TECH_QUESTION = "Ask technical question"
SERVICE_OPT_CHANGE_CONTACT_INFO = "Change contact information"

SERVICE_OPTIONS = [
    SERVICE_OPT_CHANGE_CONTACT_INFO,
    SERVICE_OPT_TECH_QUESTION,
    # "Request new airplane"
]


def conduct_service_call(
    service_options: list[str],
    person_information: PersonInformation
) -> None:
    console = Console()
    with console.status("Initializing...") as status:
        conductor = ServiceCallConductor(service_options)
    conductor.greet(person_information)

    if not conductor.has_selected_option():
        conductor.present_options_and_ask_to_choose()
        if not conductor.has_selected_option():
            conductor.communicate_abrupt_end_of_service()
            return

    while conductor.has_selected_option():
        selected_option = conductor.get_selected_option()
        print(f"Service to be performed: {selected_option}")
        if SERVICE_OPT_TECH_QUESTION == selected_option:
            conductor.answer_technical_question(person_information)
        else:
            conductor.fake_perform_service(person_information)
        # conductor.ask_for_additional_services()
        conductor.ask_for_email_services()

    conductor.ask_for_final_feedback_and_finish(person_information)


def main() -> None:
    person_information = PersonInformation("Michael")
    conduct_service_call(SERVICE_OPTIONS, person_information)


if __name__ == "__main__":
    main()
