from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from ..models import Todos, Users
import pytest
from ..routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass = StaticPool,

)


TestingSesionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSesionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'nescafetest', 'id': 1, 'user_role': 'admin'}



client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title = 'Learn to code',
        description = 'Need to learn everyday!',
        priority = 5,
        complete = False,
        owner_id = 1,
    )

    db = TestingSesionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()



@pytest.fixture
def test_user():
    user = Users(
        username = 'nescafe',
        email = 'nesk.company@gmail.com',
        first_name = 'Nestor',
        last_name = 'Juarez',
        hashed_password = bcrypt_context.hash('nescafe'),
        role = 'admin',
        phone_number = '7776001153',
        )
    db = TestingSesionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()