import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from brain_agriculture.app import app
from brain_agriculture.database import get_session
from brain_agriculture.models import User, Farmer, table_registry
from brain_agriculture.security import get_password_hash
from brain_agriculture.settings import Settings


settings = Settings()


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(settings.DATABASE_URL)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password_clean = '123456'
    hashed_password = get_password_hash(password_clean)

    user = User(
        username='felipe', email='felipe@test.com', password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password_clean

    return user


@pytest.fixture
def farmer(session):
    farmer = Farmer(
        ndoc='12345678910',
        name='Felipe da Silva',
        farm_name='Fazenda da Silva',
        city='Sao Paulo',
        state='SP',
        total_area=100,
        arable_area=50,
        vegetation_area=50,
        planted_crops='Soja, Milho',
    )
    session.add(farmer)
    session.commit()
    session.refresh(farmer)

    return farmer


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
