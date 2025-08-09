"""Shared fixtures for tests."""
# tests/conftest.py
import sys
from pathlib import Path

# Add the project's src/ directory to sys.path so that `import src.*` works
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))




