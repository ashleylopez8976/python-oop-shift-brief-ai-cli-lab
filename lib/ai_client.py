import ollama


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        user_message = {
            "role": "user",
            "content": prompt.strip(),
        }

        previous_count = len(self.history)
        self.history.append(user_message)

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.history,
            )

            if isinstance(response, dict):
                message = response.get("message")
            else:
                message = getattr(response, "message", None)

            if isinstance(message, dict):
                content = message.get("content")
            else:
                content = getattr(message, "content", None)

            if not isinstance(content, str) or not content.strip():
                raise ValueError("AI service returned no usable response.")

            self.history.append({
                "role": "assistant",
                "content": content,
            })

            return content

        except Exception as error:
            del self.history[previous_count:]
            raise RuntimeError(
                f"AI service request failed: {error}"
            ) from error

    def reset(self):
        self.history.clear()

    def message_count(self):
        return len(self.history)

    def get_transcript(self):
        return [message.copy() for message in self.history]