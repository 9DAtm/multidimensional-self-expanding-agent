import asyncio
import json

class LLMAdapter:
    def __init__(self, config):
        self.config = config
        self._client = None

    @property
    def enabled(self):
        return self.config.enabled

    async def complete(self, prompt: str) -> str:
        if not self.enabled:
            return ""

        if self.config.provider == "ollama":
            return await self._ollama(prompt)
        elif self.config.provider == "anthropic":
            return await self._anthropic(prompt)
        elif self.config.provider == "openai":
            return await self._openai(prompt)
        return ""

    async def _ollama(self, prompt: str) -> str:
        try:
            proc = await asyncio.create_subprocess_exec(
                "curl", "-s", "http://localhost:11434/api/generate",
                "-d", json.dumps({
                    "model": self.config.model or "llama3",
                    "prompt": prompt,
                    "stream": False,
                }),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            data = json.loads(stdout.decode())
            return data.get("response", "")
        except Exception:
            return "[ollama unavailable]"

    async def _anthropic(self, prompt: str) -> str:
        try:
            proc = await asyncio.create_subprocess_exec(
                "curl", "-s", "https://api.anthropic.com/v1/messages",
                "-H", f"x-api-key: {self.config.api_key}",
                "-H", "anthropic-version: 2023-06-01",
                "-H", "content-type: application/json",
                "-d", json.dumps({
                    "model": self.config.model or "claude-sonnet-4-20250514",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": prompt}],
                }),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            data = json.loads(stdout.decode())
            content = data.get("content", [])
            return content[0]["text"] if content else ""
        except Exception:
            return "[anthropic unavailable]"

    async def _openai(self, prompt: str) -> str:
        try:
            proc = await asyncio.create_subprocess_exec(
                "curl", "-s", "https://api.openai.com/v1/chat/completions",
                "-H", f"Authorization: Bearer {self.config.api_key}",
                "-H", "content-type: application/json",
                "-d", json.dumps({
                    "model": self.config.model or "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1024,
                }),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            data = json.loads(stdout.decode())
            choices = data.get("choices", [])
            return choices[0]["message"]["content"] if choices else ""
        except Exception:
            return "[openai unavailable]"