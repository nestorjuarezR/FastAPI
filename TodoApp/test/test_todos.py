from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos

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

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


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

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code', 'description': 'Need to learn everyday!', 'id': 1, 'priority': 5, 'owner_id': 1}]




def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.post("/todo/", json = request_data)
    assert response.status_code == 201

    db = TestingSesionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 
                                'title': 'Learn to code', 
                                'description': 'Need to learn everyday!', 
                                'id': 1, 
                                'priority': 5, 
                                'owner_id': 1}


def test_update_todo(test_todo):
    resquest_data = {
        'title' : 'change the title of the todo',
        'description' : 'Need to learn',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todo/1', json=resquest_data)
    assert response.status_code == 204
    db = TestingSesionLocal()
    model = db.query(Todos). filter(Todos.id == 1).first()
    assert model.title == 'change the title of the todo'
