# Contributing

Thank you for your interest in contributing to this research project.

## Getting Started

1. Fork the repository and clone your fork locally.
2. Create a virtual environment and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Place or symlink the Chest X-Ray Pneumonia dataset under `data/train`, `data/val`, and `data/test`.

## Development Workflow

1. Create a feature branch from `main`.
2. Make focused changes that preserve existing model behavior unless the change is explicitly documented.
3. Run the test suite before opening a pull request:

   ```bash
   python -m pytest tests/ -v
   ```

4. Ensure scripts still run from both legacy entry points (`python train.py`) and module paths (`python -m training.train`).

## Code Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) style.
- Add docstrings to new classes and public functions.
- Use type hints where practical.
- Do not commit datasets, checkpoints, or generated figures.
- Do not change model algorithms without discussion in an issue first.

## Pull Request Checklist

- [ ] Imports updated for any moved modules
- [ ] Tests pass locally
- [ ] No secrets, credentials, or large binary artifacts included
- [ ] README or docs updated if behavior or CLI changes

## Reporting Issues

Please include:

- Python and PyTorch versions
- Operating system
- Command used and full traceback
- Whether GPU or CPU was used

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
