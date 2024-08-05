from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

@app.get("7healthy")
def health_check():
    return {'status': 'Healthy'}

#Load router
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

