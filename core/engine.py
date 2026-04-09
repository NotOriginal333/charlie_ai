import logging
from typing import Tuple

from core.models import LessonState, LessonContext
from core.llm_client import CharlieLLMClient
from core.config import Config

logger = logging.getLogger(__name__)


class CharlieAIEngine:
    def __init__(self, llm_client: CharlieLLMClient) -> None:
        self.llm_client = llm_client

    def process_turn(self, user_input: str, context: LessonContext) -> Tuple[str, LessonContext]:
        if not context.vocabulary:
            return "Developer error: Lesson vocabulary is empty.", context

        if context.state == LessonState.GREETING:
            context.state = LessonState.PRESENTATION
            response = self.llm_client.generate_response(intent="greeting")
            return response, context

        if context.state == LessonState.PRESENTATION:
            word = context.current_word

            if word is None:
                logger.error("State machine out of sync: no word found during presentation.")
                context.state = LessonState.GOODBYE
                return self.llm_client.generate_response(intent="goodbye"), context

            context.state = LessonState.PRACTICE
            response = self.llm_client.generate_response(intent="presenting", target_word=word)
            return response, context

        if context.state == LessonState.PRACTICE:
            word = context.current_word

            if word is None:
                logger.error("State machine out of sync: no word found during practice.")
                context.state = LessonState.GOODBYE
                return self.llm_client.generate_response(intent="goodbye"), context

            intent_data = self.llm_client.analyze_intent(user_input, target_word=word)
            intent = intent_data.get("intent", "incorrect")

            if intent == "correct":
                context.current_word_index += 1
                context.retries = 0

                if context.current_word_index >= len(context.vocabulary):
                    context.state = LessonState.GOODBYE
                else:
                    context.state = LessonState.PRESENTATION

                response = self.llm_client.generate_response(intent="correct", target_word=word)
            else:
                context.retries += 1

                if context.retries >= Config.MAX_RETRIES_PER_WORD:
                    context.current_word_index += 1
                    context.retries = 0

                    if context.current_word_index >= len(context.vocabulary):
                        context.state = LessonState.GOODBYE
                    else:
                        context.state = LessonState.PRESENTATION

                    response = self.llm_client.generate_response(intent="give_up_and_move_on", target_word=word)
                else:
                    response = self.llm_client.generate_response(intent=intent, target_word=word)

            return response, context

        if context.state == LessonState.GOODBYE:
            response = self.llm_client.generate_response(intent="goodbye")
            return response, context

        return "Oops, something went wrong with the lesson state!", context
