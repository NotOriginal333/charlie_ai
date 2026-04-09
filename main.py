import logging
from core.models import LessonContext, LessonState
from core.llm_client import CharlieLLMClient
from core.engine import CharlieAIEngine

logging.basicConfig(level=logging.WARNING, format="%(message)s")


def main() -> None:
    print("=== Welcome to Charlie AI Local Tester ===")
    print("Type your responses as if you were a 4-8 year old kid.")
    print("Type 'quit' or 'exit' to stop.\n")

    client = CharlieLLMClient()
    engine = CharlieAIEngine(llm_client=client)
    context = LessonContext(vocabulary=["cat", "dog", "bird"])

    while True:
        if context.state == LessonState.GOODBYE:
            response, context = engine.process_turn(user_input="", context=context)
            print(f"Charlie: {response}\n")
            break

        if context.state in [LessonState.GREETING, LessonState.PRESENTATION]:
            response, context = engine.process_turn(user_input="", context=context)
            print(f"Charlie: {response}")
            continue

        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit']:
            print("\nExiting tester...")
            break

        print(f"\n[DEBUG] Evaluating your input for word: '{context.current_word}'")
        print("...Charlie is thinking...")

        response, context = engine.process_turn(user_input=user_input, context=context)
        print(f"Charlie: {response}")


if __name__ == "__main__":
    main()
