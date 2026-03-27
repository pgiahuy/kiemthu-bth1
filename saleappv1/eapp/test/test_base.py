import pytest
from flask import Flask

from eapp import db
from eapp.index import register_routes

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config['PAGE_SIZE'] = 2
    app.config['TESTING'] = True
    app.secret_key = 'hduageifghegehsghe8ghe8ghe89ye8a9y'
    db.init_app(app)

    register_routes(app=app)

    return app


@pytest.fixture
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def mock_cloudinary(monkeypatch):
    def fake_upload(file):
        return {'secure_url':'https://img.png'}

    monkeypatch.setattr('cloudinary.uploader.upload', fake_upload)