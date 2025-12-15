import requests
import os
import json

class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
        self.default_model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT", 300))

    def generate(self, prompt: str, model: str = None):
        model = model or self.default_model

        try:
            with requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt},
                timeout=self.timeout,
                stream=True,
            ) as response:

                response.raise_for_status()

                final_text = ""

                # Parse NDJSON streaming chunks
                for line in response.iter_lines():
                    if not line:
                        continue

                    try:
                        data = json.loads(line.decode("utf-8"))
                    except Exception:
                        continue

                    # Streaming partial chunks use "response"
                    if "response" in data:
                        final_text += data["response"]

                    # "done": true marks the end
                    if data.get("done"):
                        break

                return final_text

        except requests.exceptions.Timeout:
            raise RuntimeError(
                f"Ollama timed out after {self.timeout} seconds. "
                "Use a smaller model or increase OLLAMA_TIMEOUT."
            )

        except requests.exceptions.HTTPError as e:
            try:
                err_detail = response.json()
            except Exception:
                err_detail = response.text

            raise RuntimeError(f"Ollama error: {err_detail}") from e

    def chat(self, messages, model: str = None):
        # Convert structured messages to a natural chat-style prompt
        formatted = ""
        for m in messages:
            formatted += f"{m['role'].upper()}: {m['content']}\n"
        formatted += "ASSISTANT:"

        return self.generate(formatted, model)
