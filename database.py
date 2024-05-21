from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
# flask_sqlalchemy package provides an easy way to interact with a database using SQLAlchemy
# SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Todo(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)

    def __str__(self):
        return self.name