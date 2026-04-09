import json
import logging
from typing import Optional

from groq import Groq, APIError

from core.config import Config
from core.prompts import EVALUATOR_SYSTEM_PROMPT, PERSONA_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class CharlieLLMClient:
    def __init__(self) -> None:
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def analyze_intent(self, user_input: str, target_word: str) -> dict:
        safe_input = user_input.strip() if user_input.strip() else "(silence)"
        user_prompt = f"Target word is: '{target_word}'. The kid said: '{safe_input}'. Analyze the intent."

        try:
            response = self.client.chat.completions.create(
                model=Config.EVALUATOR_MODEL,
                messages=[
                    {"role": "system", "content": EVALUATOR_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            return json.loads(content) if content else {"intent": "incorrect"}

        except (APIError, json.JSONDecodeError) as e:
            logger.error(f"Groq API/JSON Error (Intent): {e}")
            return {"intent": "incorrect"}

    def generate_response(self, intent: str, target_word: Optional[str] = None,
                          user_input: Optional[str] = None) -> str:
        kid_said = f" The kid just said: '{user_input}'." if user_input else ""

        instructions = {
            "greeting": "Introduce yourself briefly as Charlie the fox and ask if they want to play a game.",
            "presenting": f"Excitedly point out the word '{target_word}' and ask the kid to say it.",
            "correct": f"Praise them enthusiastically for correctly saying '{target_word}'!",
            "incorrect": f"Gently encourage them to try saying '{target_word}' "
                         f"again.{kid_said} Do not say they are wrong.",
            "off_topic": f"Acknowledge what they said briefly and positively."
                         f"{kid_said} Then gently redirect their attention back to the word '{target_word}'.",
            "silence": f"Ask if they are still there and prompt them to say '{target_word}'.",
            "give_up_and_move_on": "Gently say let's try a new word.",
            "goodbye": "Congratulate them on finishing the lesson and say goodbye nicely."
        }

        specific_instruction = instructions.get(intent, instructions["incorrect"])
        user_prompt = f"Context: {specific_instruction}\nWrite Charlie's exact response now."

        try:
            response = self.client.chat.completions.create(
                model=Config.GENERATOR_MODEL,
                messages=[
                    {"role": "system", "content": PERSONA_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )

            content = response.choices[0].message.content
            return content.strip() if content else "Oops, connection error."

        except APIError as e:
            logger.error(f"Groq API Error (Generate): {e}")
            return "Oops, my connection dropped!"
