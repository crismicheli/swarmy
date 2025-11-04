# Contributing to Swarmy

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

We use GitHub to host code, track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code lints
5. Issue that pull request!

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Git

### Development Setup

```bash
# Clone the repository
git clone https://github.com/crismicheli/swarmy.git
cd swarmy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from swarmy import SwarmSimulation; print('Success!')"
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=swarmy --cov-report=html

# Run specific test
pytest tests/unit/test_agent.py
```

### Code Style

We follow PEP 8 and use Black for code formatting.

```bash
# Format code with Black
black swarmy/ tests/

# Check formatting
black --check swarmy/ tests/

# Lint with flake8
flake8 swarmy/ tests/

# Type checking with mypy
mypy swarmy/
```

## Pull Request Process

1. **Update documentation** if you change functionality
2. **Add tests** for any new features
3. **Update the CHANGELOG.md** with notes on your changes
4. **Ensure all tests pass**:
   ```bash
   pytest tests/ --cov=swarmy
   ```
5. **Format your code**:
   ```bash
   black swarmy/
   ```

## Reporting Bugs

When creating an issue, please include:

- **Description**: What is the bug?
- **Steps to reproduce**: How can we reproduce it?
- **Expected behavior**: What should happen?
- **Actual behavior**: What actually happened?
- **Environment**: Python version, OS, etc.
- **Code snippet**: Minimal code that demonstrates the issue

## Suggesting Enhancements

Include:

- **Use case**: Why do you need this?
- **Proposed solution**: How should it work?
- **Alternatives**: Any other approaches?
- **Context**: Why is this important?

## Coding Standards

### Naming Conventions
- Classes: `PascalCase` (e.g., `Agent`, `Queen`)
- Functions/methods: `snake_case` (e.g., `get_state()`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_RADIUS`)
- Private methods: `_leading_underscore` (e.g., `_process_communications()`)

### Docstrings
All public classes and functions should have docstrings:

```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
```

### Type Hints
Use type hints for better code clarity:

```python
from typing import List, Dict, Tuple

def process_data(
    agents: List[Agent],
    config: Dict[str, float]
) -> Tuple[int, float]:
    """Process agent data."""
```

## Testing Guidelines

- Write tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names: `test_agent_moves_forward_when_commanded()`
- Test both happy paths and edge cases

```python
def test_agent_collision_resets_counter():
    """Test that collision resets counter for target."""
    agent = Agent(position=(0, 0), ...)
    agent.collision_with_target('queen')
    assert agent.counters['queen'] == 0
```

## Documentation

- Keep README.md up to date
- Document new parameters in docstrings
- Update CHANGELOG.md with new features
- Add examples for complex functionality

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Code of Conduct

- Be respectful and inclusive
- Assume good faith
- Criticize ideas, not people
- Welcome newcomers and help them get started

Thank you for contributing to Swarmy! 🎉
