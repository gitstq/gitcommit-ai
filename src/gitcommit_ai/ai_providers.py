"""AI provider implementations for generating commit messages."""

import json
from abc import ABC, abstractmethod
from typing import Optional

import httpx

from .config import AIProviderConfig


class AIProviderError(Exception):
    """Custom exception for AI provider errors."""
    pass


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, config: AIProviderConfig):
        self.config = config
    
    @abstractmethod
    async def generate_commit_message(
        self, 
        diff: str, 
        language: str = "zh",
        context: Optional[str] = None
    ) -> str:
        """Generate a commit message from the diff."""
        pass
    
    def _build_prompt(self, diff: str, language: str, context: Optional[str] = None) -> str:
        """Build the prompt for the AI model."""
        
        lang_instruction = "中文" if language == "zh" else "English"
        
        prompt = f"""You are a helpful assistant that writes clear and concise git commit messages.

Please analyze the following git diff and generate a commit message following the Conventional Commits specification.

The commit message should be in {lang_instruction}.

## Conventional Commits Format:
<type>(<scope>): <description>

[optional body]

[optional footer(s)]

## Types:
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code
- refactor: A code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- test: Adding missing tests or correcting existing tests
- chore: Changes to the build process or auxiliary tools

## Guidelines:
1. Use imperative mood (e.g., "add" not "added")
2. Keep the description concise (max 50 chars for subject)
3. Focus on WHAT changed and WHY, not HOW
4. If there are multiple changes, summarize them

"""
        
        if context:
            prompt += f"\n## Additional Context:\n{context}\n"
        
        prompt += f"""
## Git Diff:
```diff
{diff}
```

Please generate ONLY the commit message (subject line only, no body needed unless necessary).
Do not include any explanations or markdown formatting.
"""
        
        return prompt


class OpenAIProvider(AIProvider):
    """OpenAI API provider."""
    
    async def generate_commit_message(
        self, 
        diff: str, 
        language: str = "zh",
        context: Optional[str] = None
    ) -> str:
        if not self.config.api_key:
            raise AIProviderError("OpenAI API key is required")
        
        prompt = self._build_prompt(diff, language, context)
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that writes git commit messages."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        base_url = self.config.base_url or "https://api.openai.com/v1"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                
                message = data["choices"][0]["message"]["content"].strip()
                # Clean up the message
                message = message.strip('"').strip("'")
                return message
            except httpx.HTTPStatusError as e:
                raise AIProviderError(f"OpenAI API error: {e.response.text}")
            except Exception as e:
                raise AIProviderError(f"Failed to generate commit message: {e}")


class ClaudeProvider(AIProvider):
    """Anthropic Claude API provider."""
    
    async def generate_commit_message(
        self, 
        diff: str, 
        language: str = "zh",
        context: Optional[str] = None
    ) -> str:
        if not self.config.api_key:
            raise AIProviderError("Anthropic API key is required")
        
        prompt = self._build_prompt(diff, language, context)
        
        headers = {
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        base_url = self.config.base_url or "https://api.anthropic.com"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{base_url}/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                
                message = data["content"][0]["text"].strip()
                message = message.strip('"').strip("'")
                return message
            except httpx.HTTPStatusError as e:
                raise AIProviderError(f"Claude API error: {e.response.text}")
            except Exception as e:
                raise AIProviderError(f"Failed to generate commit message: {e}")


class OllamaProvider(AIProvider):
    """Ollama local API provider."""
    
    async def generate_commit_message(
        self, 
        diff: str, 
        language: str = "zh",
        context: Optional[str] = None
    ) -> str:
        prompt = self._build_prompt(diff, language, context)
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature
            }
        }
        
        base_url = self.config.base_url or "http://localhost:11434"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{base_url}/api/generate",
                    headers=headers,
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()
                
                message = data["response"].strip()
                message = message.strip('"').strip("'")
                return message
            except httpx.HTTPStatusError as e:
                raise AIProviderError(f"Ollama API error: {e.response.text}")
            except Exception as e:
                raise AIProviderError(f"Failed to generate commit message: {e}")


class OpenRouterProvider(AIProvider):
    """OpenRouter API provider."""
    
    async def generate_commit_message(
        self, 
        diff: str, 
        language: str = "zh",
        context: Optional[str] = None
    ) -> str:
        if not self.config.api_key:
            raise AIProviderError("OpenRouter API key is required")
        
        prompt = self._build_prompt(diff, language, context)
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/gitcommit-ai",
            "X-Title": "GitCommit AI"
        }
        
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that writes git commit messages."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        base_url = self.config.base_url or "https://openrouter.ai/api/v1"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                
                message = data["choices"][0]["message"]["content"].strip()
                message = message.strip('"').strip("'")
                return message
            except httpx.HTTPStatusError as e:
                raise AIProviderError(f"OpenRouter API error: {e.response.text}")
            except Exception as e:
                raise AIProviderError(f"Failed to generate commit message: {e}")


class DeepSeekProvider(AIProvider):
    """DeepSeek API provider."""
    
    async def generate_commit_message(
        self, 
        diff: str, 
        language: str = "zh",
        context: Optional[str] = None
    ) -> str:
        if not self.config.api_key:
            raise AIProviderError("DeepSeek API key is required")
        
        prompt = self._build_prompt(diff, language, context)
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that writes git commit messages."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        base_url = self.config.base_url or "https://api.deepseek.com"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                
                message = data["choices"][0]["message"]["content"].strip()
                message = message.strip('"').strip("'")
                return message
            except httpx.HTTPStatusError as e:
                raise AIProviderError(f"DeepSeek API error: {e.response.text}")
            except Exception as e:
                raise AIProviderError(f"Failed to generate commit message: {e}")


def get_provider(name: str, config: AIProviderConfig) -> AIProvider:
    """Get an AI provider by name."""
    providers = {
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "ollama": OllamaProvider,
        "openrouter": OpenRouterProvider,
        "deepseek": DeepSeekProvider,
    }
    
    if name not in providers:
        raise AIProviderError(f"Unknown provider: {name}. Available: {list(providers.keys())}")
    
    return providers[name](config)
