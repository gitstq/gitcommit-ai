"""Configuration management for GitCommit AI."""

import os
from pathlib import Path
from typing import Optional

import toml
from pydantic import BaseModel, Field


class AIProviderConfig(BaseModel):
    """Configuration for an AI provider."""
    
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 500


class Config(BaseModel):
    """Main configuration class."""
    
    # Default provider
    default_provider: str = Field(default="openai", description="Default AI provider to use")
    
    # Language preference
    language: str = Field(default="zh", description="Language for commit messages (zh/en)")
    
    # Auto commit without confirmation
    auto_commit: bool = Field(default=False, description="Skip confirmation prompt")
    
    # Providers configuration
    providers: dict[str, AIProviderConfig] = Field(
        default_factory=lambda: {
            "openai": AIProviderConfig(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4o-mini"
            ),
            "claude": AIProviderConfig(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                base_url="https://api.anthropic.com",
                model="claude-3-haiku-20240307"
            ),
            "ollama": AIProviderConfig(
                base_url="http://localhost:11434",
                model="llama3.2"
            ),
            "openrouter": AIProviderConfig(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                model="anthropic/claude-3-haiku"
            ),
            "deepseek": AIProviderConfig(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com",
                model="deepseek-chat"
            ),
        }
    )
    
    # Commit message style
    commit_style: str = Field(default="conventional", description="Commit message style")
    
    # Max diff size (in characters)
    max_diff_size: int = Field(default=8000, description="Maximum diff size to analyze")
    
    @classmethod
    def get_config_path(cls) -> Path:
        """Get the configuration file path."""
        # Check for local config first
        local_config = Path(".gitcommit-ai.toml")
        if local_config.exists():
            return local_config
        
        # Then check for global config
        home = Path.home()
        global_config = home / ".config" / "gitcommit-ai" / "config.toml"
        return global_config
    
    @classmethod
    def load(cls) -> "Config":
        """Load configuration from file or create default."""
        config_path = cls.get_config_path()
        
        if config_path.exists():
            try:
                data = toml.load(config_path)
                return cls(**data)
            except Exception as e:
                print(f"Warning: Failed to load config from {config_path}: {e}")
                return cls()
        
        return cls()
    
    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if path is None:
            path = self.get_config_path()
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict and save
        data = self.model_dump()
        with open(path, "w") as f:
            toml.dump(data, f)
    
    def get_provider_config(self, provider: Optional[str] = None) -> AIProviderConfig:
        """Get configuration for a specific provider."""
        if provider is None:
            provider = self.default_provider
        
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        
        return self.providers[provider]
