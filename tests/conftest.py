import pytest

from app import app, db


def create_app():
    """Return Flask's app object with test configuration"""
    app.config.from_object("app.config.TestingConfig")
    return app


def set_up():
    """Create database tables according to the app models"""
    db.create_all()
    db.session.commit()


def tear_down():
    """Remove all tables from the database"""
    db.session.remove()
    db.drop_all()


@pytest.fixture
def client():
    """Create Flask's test client to interact with the application"""
    client = create_app().test_client()
    set_up()
    yield client
    tear_down()
