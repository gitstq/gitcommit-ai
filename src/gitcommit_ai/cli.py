"""Command-line interface for GitCommit AI."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from . import __version__
from .ai_providers import AIProviderError, get_provider
from .config import Config
from .git_utils import (
    GitError,
    commit,
    get_current_branch,
    get_git_status,
    get_recent_commits,
    get_staged_diff,
    is_git_repository,
    stage_files,
)

console = Console()


def print_banner():
    """Print the application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🤖 GitCommit AI - Smart Commit Message Generator        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def print_error(message: str):
    """Print an error message."""
    console.print(f"❌ [bold red]Error:[/bold red] {message}")


def print_success(message: str):
    """Print a success message."""
    console.print(f"✅ [bold green]{message}[/bold green]")


def print_info(message: str):
    """Print an info message."""
    console.print(f"ℹ️  [blue]{message}[/blue]")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"⚠️  [yellow]{message}[/yellow]")


async def generate_commit_message(
    config: Config,
    diff_text: str,
    provider_name: Optional[str] = None
) -> str:
    """Generate a commit message using the configured AI provider."""
    provider_name = provider_name or config.default_provider
    provider_config = config.get_provider_config(provider_name)
    
    provider = get_provider(provider_name, provider_config)
    
    with console.status(f"[bold green]Generating commit message with {provider_name}..."):
        message = await provider.generate_commit_message(
            diff=diff_text,
            language=config.language
        )
    
    return message


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version information")
@click.option("--provider", "-p", help="AI provider to use")
@click.option("--language", "-l", type=click.Choice(["zh", "en"]), help="Language for commit message")
@click.option("--auto", "-a", is_flag=True, help="Skip confirmation and commit automatically")
@click.option("--dry-run", "-d", is_flag=True, help="Show generated message without committing")
@click.pass_context
def main(ctx, version, provider, language, auto, dry_run):
    """🤖 GitCommit AI - Generate conventional commit messages with AI.
    
    Examples:
        gitcm                    # Generate commit message for staged changes
        gitcm --provider openai  # Use specific provider
        gitcm --language en      # Generate English commit message
        gitcm --auto             # Auto-commit without confirmation
        gitcm config             # Configure settings
    """
    if version:
        console.print(f"GitCommit AI version {__version__}")
        return
    
    # If no subcommand is invoked, run the main commit flow
    if ctx.invoked_subcommand is None:
        asyncio.run(commit_flow(provider, language, auto, dry_run))


async def commit_flow(provider: Optional[str], language: Optional[str], auto: bool, dry_run: bool):
    """Main commit flow."""
    print_banner()
    
    # Check if we're in a git repository
    if not is_git_repository():
        print_error("Not a git repository. Please run this command inside a git repository.")
        sys.exit(1)
    
    # Load configuration
    config = Config.load()
    
    # Override config with CLI options
    if language:
        config.language = language
    if auto:
        config.auto_commit = True
    
    # Check git status
    try:
        status = get_git_status()
    except GitError as e:
        print_error(str(e))
        sys.exit(1)
    
    # Show repository info
    console.print(Panel(
        f"[bold]Branch:[/bold] {status.branch}\n"
        f"[bold]Staged:[/bold] {len(status.staged_files)} files\n"
        f"[bold]Unstaged:[/bold] {len(status.unstaged_files)} files",
        title="Repository Status",
        border_style="blue"
    ))
    
    # Check if there are staged changes
    if not status.has_staged:
        if status.has_unstaged or status.has_untracked:
            print_warning("No staged changes found.")
            
            # Ask if user wants to stage all changes
            if Confirm.ask("Would you like to stage all changes?"):
                stage_files(["."])
                print_success("All changes staged.")
                # Refresh status
                status = get_git_status()
            else:
                print_info("Please stage your changes first using 'git add'")
                sys.exit(0)
        else:
            print_info("No changes to commit.")
            sys.exit(0)
    
    # Get the diff
    try:
        diff = get_staged_diff(max_size=config.max_diff_size)
    except GitError as e:
        print_error(str(e))
        sys.exit(1)
    
    if not diff.diff_text:
        print_info("No diff to analyze.")
        sys.exit(0)
    
    # Show diff stats
    console.print(f"\n[bold]Changes:[/bold] {len(diff.files_changed)} files, "
                  f"[green]+{diff.insertions}[/green] / [red]-{diff.deletions}[/red]")
    
    # Generate commit message
    try:
        message = await generate_commit_message(config, diff.diff_text, provider)
    except AIProviderError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to generate commit message: {e}")
        sys.exit(1)
    
    # Display generated message
    console.print("\n" + Panel(
        f"[bold]{message}[/bold]",
        title="Generated Commit Message",
        border_style="green"
    ))
    
    if dry_run:
        print_info("Dry run mode - no commit was made.")
        return
    
    # Confirm or auto-commit
    if not config.auto_commit:
        if not Confirm.ask("\nDo you want to commit with this message?"):
            # Allow user to edit the message
            custom_message = Prompt.ask(
                "Enter your custom commit message (or press Enter to cancel)",
                default=""
            )
            if custom_message.strip():
                message = custom_message.strip()
            else:
                print_info("Commit cancelled.")
                return
    
    # Create the commit
    try:
        commit_hash = commit(message)
        print_success(f"Committed successfully! [dim]({commit_hash})[/dim]")
    except GitError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
def config():
    """⚙️  Configure GitCommit AI settings."""
    print_banner()
    
    config = Config.load()
    
    console.print("\n[bold]Current Configuration:[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Default Provider", config.default_provider)
    table.add_row("Language", "中文" if config.language == "zh" else "English")
    table.add_row("Auto Commit", "Yes" if config.auto_commit else "No")
    table.add_row("Max Diff Size", str(config.max_diff_size))
    
    console.print(table)
    
    console.print("\n[bold]Configured Providers:[/bold]\n")
    
    provider_table = Table(show_header=True, header_style="bold magenta")
    provider_table.add_column("Provider", style="cyan")
    provider_table.add_column("Model", style="green")
    provider_table.add_column("API Key", style="yellow")
    
    for name, provider_config in config.providers.items():
        has_key = "✓" if provider_config.api_key else "✗"
        provider_table.add_row(name, provider_config.model, has_key)
    
    console.print(provider_table)
    
    console.print("\n[dim]To edit configuration, modify the config file at:[/dim]")
    console.print(f"[blue]{Config.get_config_path()}[/blue]")


@main.command()
def status():
    """📊 Show git repository status."""
    print_banner()
    
    if not is_git_repository():
        print_error("Not a git repository.")
        sys.exit(1)
    
    try:
        git_status = get_git_status()
        branch = get_current_branch()
        recent_commits = get_recent_commits(5)
    except GitError as e:
        print_error(str(e))
        sys.exit(1)
    
    console.print(Panel(
        f"[bold]Current Branch:[/bold] {branch}",
        title="Repository Info",
        border_style="blue"
    ))
    
    # Staged files
    if git_status.staged_files:
        console.print("\n[bold green]Staged Files:[/bold green]")
        for f in git_status.staged_files:
            console.print(f"  [green]+[/green] {f}")
    
    # Unstaged files
    if git_status.unstaged_files:
        console.print("\n[bold yellow]Unstaged Files:[/bold yellow]")
        for f in git_status.unstaged_files:
            console.print(f"  [yellow]~[/yellow] {f}")
    
    # Untracked files
    if git_status.untracked_files:
        console.print("\n[bold red]Untracked Files:[/bold red]")
        for f in git_status.untracked_files:
            console.print(f"  [red]?[/red] {f}")
    
    # Recent commits
    if recent_commits:
        console.print("\n[bold]Recent Commits:[/bold]")
        for commit in recent_commits:
            console.print(f"  [dim]{commit['hash']}[/dim] {commit['message']}")


@main.command()
@click.option("--global", "global_config", is_flag=True, help="Create global configuration")
def init(global_config: bool):
    """🚀 Initialize GitCommit AI configuration."""
    print_banner()
    
    config = Config()
    
    # Ask for configuration
    console.print("\n[bold]Let's configure GitCommit AI:[/bold]\n")
    
    # Provider selection
    providers = ["openai", "claude", "ollama", "openrouter", "deepseek"]
    console.print("Available providers: " + ", ".join(providers))
    
    default_provider = Prompt.ask(
        "Select default provider",
        choices=providers,
        default="openai"
    )
    config.default_provider = default_provider
    
    # Language selection
    language = Prompt.ask(
        "Select default language",
        choices=["zh", "en"],
        default="zh"
    )
    config.language = language
    
    # API key for the selected provider
    if default_provider != "ollama":
        api_key = Prompt.ask(
            f"Enter your {default_provider} API key (or set it as environment variable)",
            password=True,
            default=""
        )
        if api_key:
            config.providers[default_provider].api_key = api_key
    
    # Save configuration
    if global_config:
        config_path = Path.home() / ".config" / "gitcommit-ai" / "config.toml"
    else:
        config_path = Path(".gitcommit-ai.toml")
    
    config.save(config_path)
    print_success(f"Configuration saved to {config_path}")


if __name__ == "__main__":
    main()
