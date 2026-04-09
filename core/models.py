from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class LessonState(str, Enum):
    GREETING = "greeting"
    PRESENTATION = "presentation"
    PRACTICE = "practice"
    GOODBYE = "goodbye"


class LessonContext(BaseModel):
    vocabulary: List[str]
    current_word_index: int = 0
    state: LessonState = LessonState.GREETING
    retries: int = 0

    @property
    def current_word(self) -> Optional[str]:
        if self.current_word_index < len(self.vocabulary):
            return self.vocabulary[self.current_word_index]
        return None
