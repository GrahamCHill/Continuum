import requests
import os

class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
        self.default_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    def generate(self, prompt: str, model: str = None):
        model = model or self.default_model

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": model, "prompt": prompt},
            timeout=60,
        )
        response.raise_for_status()

        # Ollama streams tokens, so content appears at end
        return response.json().get("response", "")

    def chat(self, messages, model: str = None):
        # Convert messages to plain prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return self.generate(prompt, model)
