from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean



class Users(Base):
    __tablename__ = 'users'             #Name of the table

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)



class Todos(Base):

    __tablename__ = 'todos'    #Set the name of the table

    #Set the Columns of the table todos
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
