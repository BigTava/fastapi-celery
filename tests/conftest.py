import os

import pytest
from pytest_factoryboy import register

from app.database import Base, SessionLocal, engine
from app.tdd.factories import MemberFactory
from app.users.factories import UserFactory

register(UserFactory)
register(MemberFactory)

os.environ["FASTAPI_CONFIG"] = "testing"  # noqa


@pytest.fixture(scope="function")
def settings():
    from app.config import settings as _settings
    return _settings


@pytest.fixture(scope="function")
def app(settings):
    from app import create_app

    app = create_app()
    return app


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(app):
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client



@pytest.fixture(autouse=True, scope="function")
def tmp_upload_dir(tmpdir, settings):
    settings.UPLOADS_DEFAULT_DEST = tmpdir.mkdir("tmp")