from pathlib import Path

DESKTOP_PATH = str(Path.home() / "Desktop")
PROTOCOL_PATH = f"{DESKTOP_PATH}/conversation_protocol.txt"
GERMAN_SUMMARY_PATH = f"{DESKTOP_PATH}/german_summary.txt"


class Config:
    def get_protocol_path(self) -> str:
        return PROTOCOL_PATH

    def get_german_summary_path(self) -> str:
        return GERMAN_SUMMARY_PATH
