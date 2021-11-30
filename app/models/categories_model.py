from dataclasses import dataclass
from typing import Text
from app.configs.database import db
from sqlalchemy.orm import validates, relationship
import psycopg2


@dataclass
class Categories(db.Model):
    id: int
    name: str
    description:str
    __tablename__ = 'categories'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    result = relationship('Tasks', secondary='tasks_categories', backref='categories')

    @validates('name')
    def validate(self, key, name):
      unique_key = (
              Categories
              .query
              .filter(Categories.name==name)
              .one_or_none()
          )
      if unique_key is not None:
        raise psycopg2.errors.UniqueViolation ("Category already exists")
      return name