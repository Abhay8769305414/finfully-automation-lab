import os
import pytest
from pathlib import Path

@pytest.fixture(autouse=True)
def set_project_root(monkeypatch):
    """Ensure all tests run with CWD = project root (finfully-automation-lab/)."""
    project_root = Path(__file__).parent
    monkeypatch.chdir(project_root)
    # Default unit tests to SQLite & eager mode unless overridden
    if os.getenv("DATABASE_BACKEND") != "postgres":
        monkeypatch.setenv("DATABASE_BACKEND", "sqlite")
        monkeypatch.setenv("CELERY_TASK_ALWAYS_EAGER", "true")
        from src.config import Config
        Config.DATABASE_BACKEND = "sqlite"
