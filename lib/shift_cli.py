from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        self.ai_client = ai_client
        self.brief_builder = (
            brief_builder
            if brief_builder is not None
            else HandoffBriefBuilder()
        )
        self.running = True

    def display_welcome(self):
        print("Welcome to the Shift Handoff Brief CLI!")
        print(self.command_help())

    def command_help(self):
        return (
            "Available commands:\n"
            "brief <shift notes> - Create a shift handoff brief\n"
            "revise <feedback> - Revise the previous brief\n"
            "history - Show the conversation message count\n"
            "reset - Clear conversation history\n"
            "help - Show available commands\n"
            "exit - Exit the application\n"
            "quit - Exit the application"
        )

    def handle_command(self, raw_input):
        if not isinstance(raw_input, str) or not raw_input.strip():
            return "Input Error: Please enter a command."

        parts = raw_input.strip().split(maxsplit=1)
        command = parts[0].lower()
        payload = parts[1].strip() if len(parts) > 1 else ""

        try:
            if command == "brief":
                if not payload:
                    raise ValueError("Shift notes cannot be empty")

                return self.brief_builder.create_brief(
                    self.ai_client, payload
                )

            if command == "revise":
                if not payload:
                    raise ValueError("Revision feedback cannot be empty")

                return self.brief_builder.revise_brief(
                    self.ai_client, payload
                )

            if command == "history":
                count = self.ai_client.message_count()
                return f"Conversation messages: {count}"

            if command == "reset":
                self.ai_client.reset()
                return "Conversation history reset."

            if command == "help":
                return self.command_help()

            if command in ("exit", "quit"):
                self.running = False
                return "Goodbye!"

            return (
                f"Input Error: Unknown command '{command}'. "
                "Type 'help' for available commands."
            )

        except ValueError as error:
            return f"Input Error: {error}"

        except RuntimeError as error:
            return f"Service Error: {error}"

    def run(self):
        self.display_welcome()

        while self.running:
            try:
                user_input = input("> ")
            except EOFError:
                self.running = False
                break

            result = self.handle_command(user_input)

            if result is not None:
                print(result)


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()