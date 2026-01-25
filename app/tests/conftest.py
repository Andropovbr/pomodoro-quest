import os
from pathlib import Path

# Use a file-based SQLite DB for tests.
# In-memory SQLite is per-connection, which breaks when the app opens multiple connections.
test_db_path = Path("/tmp/pomodoro_quest_test.sqlite")

# Ensure a clean DB for each test run.
if test_db_path.exists():
    test_db_path.unlink()

os.environ["DATABASE_URL"] = f"sqlite:///{test_db_path}"
os.environ["LOG_LEVEL"] = "WARNING"
