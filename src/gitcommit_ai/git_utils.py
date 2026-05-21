"""Git utilities for analyzing repository changes."""

import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class GitStatus:
    """Represents the git status of a repository."""
    
    branch: str
    has_staged: bool
    has_unstaged: bool
    has_untracked: bool
    staged_files: list[str]
    unstaged_files: list[str]
    untracked_files: list[str]


@dataclass
class GitDiff:
    """Represents git diff information."""
    
    files_changed: list[str]
    insertions: int
    deletions: int
    diff_text: str


class GitError(Exception):
    """Custom exception for git-related errors."""
    pass


def run_git_command(args: list[str], cwd: Optional[str] = None) -> str:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise GitError(f"Git command failed: {e.stderr}")
    except FileNotFoundError:
        raise GitError("Git is not installed or not in PATH")


def is_git_repository(cwd: Optional[str] = None) -> bool:
    """Check if the current directory is a git repository."""
    try:
        run_git_command(["rev-parse", "--git-dir"], cwd=cwd)
        return True
    except GitError:
        return False


def get_current_branch(cwd: Optional[str] = None) -> str:
    """Get the current git branch name."""
    try:
        return run_git_command(["branch", "--show-current"], cwd=cwd)
    except GitError:
        # Try to get from detached HEAD
        try:
            return run_git_command(["rev-parse", "--short", "HEAD"], cwd=cwd)
        except GitError:
            return "unknown"


def get_git_status(cwd: Optional[str] = None) -> GitStatus:
    """Get the current git status."""
    branch = get_current_branch(cwd)
    
    # Get staged files
    staged_output = run_git_command(["diff", "--cached", "--name-only"], cwd=cwd)
    staged_files = [f for f in staged_output.split("\n") if f] if staged_output else []
    
    # Get unstaged files
    unstaged_output = run_git_command(["diff", "--name-only"], cwd=cwd)
    unstaged_files = [f for f in unstaged_output.split("\n") if f] if unstaged_output else []
    
    # Get untracked files
    untracked_output = run_git_command(
        ["ls-files", "--others", "--exclude-standard"], cwd=cwd
    )
    untracked_files = [f for f in untracked_output.split("\n") if f] if untracked_output else []
    
    return GitStatus(
        branch=branch,
        has_staged=len(staged_files) > 0,
        has_unstaged=len(unstaged_files) > 0,
        has_untracked=len(untracked_files) > 0,
        staged_files=staged_files,
        unstaged_files=unstaged_files,
        untracked_files=untracked_files
    )


def get_staged_diff(cwd: Optional[str] = None, max_size: int = 8000) -> GitDiff:
    """Get the diff of staged changes."""
    diff_output = run_git_command(["diff", "--cached"], cwd=cwd)
    
    if not diff_output:
        return GitDiff(files_changed=[], insertions=0, deletions=0, diff_text="")
    
    # Get stats
    stats_output = run_git_command(["diff", "--cached", "--stat"], cwd=cwd)
    
    # Parse stats
    files_changed = []
    insertions = 0
    deletions = 0
    
    for line in stats_output.split("\n"):
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 2:
                filename = parts[0].strip()
                files_changed.append(filename)
                
                # Parse insertions/deletions
                stats_part = parts[1].strip()
                if "insertion" in stats_part:
                    try:
                        insertions += int(stats_part.split()[0])
                    except (ValueError, IndexError):
                        pass
                if "deletion" in stats_part:
                    try:
                        deletions += int(stats_part.split()[0])
                    except (ValueError, IndexError):
                        pass
    
    # Truncate diff if too large
    diff_text = diff_output
    if len(diff_text) > max_size:
        diff_text = diff_text[:max_size] + "\n... (diff truncated)"
    
    return GitDiff(
        files_changed=files_changed,
        insertions=insertions,
        deletions=deletions,
        diff_text=diff_text
    )


def stage_files(files: list[str], cwd: Optional[str] = None) -> None:
    """Stage files for commit."""
    if files:
        run_git_command(["add"] + files, cwd=cwd)


def commit(message: str, cwd: Optional[str] = None) -> str:
    """Create a commit with the given message."""
    run_git_command(["commit", "-m", message], cwd=cwd)
    
    # Get the commit hash
    return run_git_command(["rev-parse", "--short", "HEAD"], cwd=cwd)


def get_recent_commits(n: int = 5, cwd: Optional[str] = None) -> list[dict]:
    """Get recent commits for context."""
    try:
        output = run_git_command(
            ["log", f"-{n}", "--pretty=format:%h|%s|%an|%ad", "--date=short"],
            cwd=cwd
        )
        
        commits = []
        for line in output.split("\n"):
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 4:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1],
                        "author": parts[2],
                        "date": parts[3]
                    })
        
        return commits
    except GitError:
        return []
