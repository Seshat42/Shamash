import os
import importlib
import pytest


@pytest.fixture(autouse=True)
def temp_db(tmp_path):
    db_file = tmp_path / "test.db"
    os.environ["SHAMASH_DB_PATH"] = str(db_file)
    import server.db as db

    importlib.reload(db)
    yield db
    db.engine.dispose()
    os.environ.pop("SHAMASH_DB_PATH")
