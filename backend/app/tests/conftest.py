import pytest
import app.config as config
import app.db as db


@pytest.fixture()
def tmp_db(tmp_path, monkeypatch):
    p = tmp_path / "test.db"
    monkeypatch.setattr(config, "DB_PATH", p)
    monkeypatch.setattr(db, "DB_PATH", p)
    from app import seed
    seed.init_db()
    return p
