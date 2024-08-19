
from ..routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user




def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code', 'description': 'Need to learn everyday!', 'id': 1, 'priority': 5, 'owner_id': 1}]




def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.post("/todos/", json = request_data)
    assert response.status_code == 201

    db = TestingSesionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
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

    response = client.put('/todos/todo/1', json=resquest_data)
    assert response.status_code == 204
    db = TestingSesionLocal()
    model = db.query(Todos). filter(Todos.id == 1).first()
    assert model.title == 'change the title of the todo'
