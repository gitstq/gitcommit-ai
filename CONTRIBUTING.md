# Contributing to GitCommit AI

Thank you for your interest in contributing to GitCommit AI! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [issue tracker](https://github.com/yourusername/gitcommit-ai/issues)
2. If not, create a new issue with:
   - Clear description of the problem/suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature/fix: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Format your code: `black src/`
6. Commit with a clear message following [Conventional Commits](https://www.conventionalcommits.org/)
7. Push to your fork and submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/gitcommit-ai.git
cd gitcommit-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style

- Follow PEP 8 guidelines
- Use `black` for code formatting
- Use `ruff` for linting
- Add type hints where appropriate
- Write docstrings for public functions

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

## Questions?

Feel free to open an issue for any questions or join our discussions.

Thank you for contributing! 🎉
