import os
from groq import Groq, APIConnectionError, RateLimitError

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            self.enabled = False
            return

        self.client = Groq(api_key=api_key)
        self.default_model = "qwen-2.5-32b"
        self.enabled = True

    def chat(self, messages, model=None):
        if not self.enabled:
            raise RuntimeError("groq_disabled")

        try:
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=0.2,
            )
            return response.choices[0].message["content"]

        except (APIConnectionError, RateLimitError):
            raise RuntimeError("groq_failed")

    def generate(self, prompt, model=None):
        return self.chat([{"role": "user", "content": prompt}], model)
