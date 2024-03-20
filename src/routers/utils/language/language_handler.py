from dataclasses import dataclass

from static.text.eng import ENG_BUTTONS, ENG_MESSAGES
from static.text.ru import RU_BUTTONS, RU_MESSAGES


@dataclass
class Text:
    buttons: dict[str, str]
    messages: dict[str, str]


LANGUAGES = {
    "ru": Text(buttons=RU_BUTTONS, messages=RU_MESSAGES),
    "eng": Text(buttons=ENG_BUTTONS, messages=ENG_MESSAGES),
}


def get_language(code: str):
    return LANGUAGES.get(code, LANGUAGES["eng"])
