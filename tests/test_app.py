import pytest
from flask_server.app import app, db
from sqlalchemy import text

@pytest.fixture(name = 'c')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app.test_client()
    with app.app_context():
        db.drop_all()

def test_db_connection(c):
    with app.app_context():
        try:
            result = db.session.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")