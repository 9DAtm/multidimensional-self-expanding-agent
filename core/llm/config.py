import os

class LLMConfig:
    def __init__(self, provider="none", api_key="", model=""):
        self.provider = provider
        self.api_key = api_key
        self.model = model

    @classmethod
    def from_env(cls):
        try:
            with open(".env") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())
        except FileNotFoundError:
            pass

        return cls(
            provider=os.environ.get("LLM_PROVIDER", "none"),
            api_key=os.environ.get("LLM_API_KEY", ""),
            model=os.environ.get("LLM_MODEL", ""),
        )

    @property
    def enabled(self):
        return self.provider != "none"

    def __str__(self):
        if not self.enabled:
            return "none (deterministic mode)"
        return f"{self.provider}/{self.model}"