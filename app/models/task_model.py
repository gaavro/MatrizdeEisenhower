from typing import Text
import psycopg2
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.mapper import validates
from app.configs.database import db
from app.exceptions.exceptions import InvalidImportanceOrUrgencyError, UpdateError
from app.models.categories_model import Categories
from app.models.eisehowers_model import Eisehowers
from dataclasses import dataclass




@dataclass
class Tasks(db.Model):
    id: int
    name: str
    description: str
    importance: int
    urgency: int
    eisehowers_id: int

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, default= "") 
    duration = db.Column(db.Integer) 
    importance = db.Column(db.Integer)
    urgency = db.Column(db.Integer)
    eisehowers_id = db.Column(db.Integer, db.ForeignKey('eisehowers.id'), nullable= False)
    categor = relationship("TasksCategories",cascade='all,delete-orphan', backref=backref("categories_ref", uselist=False))

    @validates('importance')
    def verify_importance(self, key, importance):
      if importance != 1 and importance != 2:
        return [1,2]

      return importance

    @validates('urgency')
    def verify_urgency(self, key, urgency):
      if urgency != 1 and urgency != 2:
        return [1,2]

      return urgency   

    @staticmethod
   
    def classify_eisenhower(data):
        if data["importance"] == 1 and data["urgency"] == 1:
            data["eisehowers_id"] = 1
            return data["eisehowers_id"]
        if data["importance"] == 1 and data["urgency"] == 2:
            data["eisehowers_id"] = 2
            return data["eisehowers_id"]
        if data["importance"] == 2 and data["urgency"] == 1:
            data["eisehowers_id"] = 3
            return data["eisehowers_id"]
        if data["importance"] == 2 and data["urgency"] == 2:
            data["eisehowers_id"] = 4
            return data["eisehowers_id"]
        raise InvalidImportanceOrUrgencyError(data["urgency"], data["importance"])

  
    @validates('name')
    def validate(self, key, name):
      unique_key = (
              Tasks
              .query
              .filter(Tasks.name==name)
              .one_or_none()
          )
      if unique_key is not None:
        raise psycopg2.errors.UniqueViolation ("Task already exists")
      return name


    @staticmethod
    def update_importance(data, current_task):
        if data["importance"] == 1 and current_task.urgency == 1:
            data["eisehowers_id"] = 1
            return data["eisenhowers_id"]
        if data["importance"] == 1 and current_task.urgency == 2:
            data["eisehowers_id"] = 2
            return data["eisehowers_id"]
        if data["importance"] == 2 and current_task.urgency == 1:
            data["eisehowers_id"] = 3
            return data["eisehowers_id"]
        if data["importance"] == 2 and current_task.urgency == 2:
            data["eisehowers_id"] = 4
            return data["eisehowers_id"]
        else:
            raise UpdateError
    @staticmethod
    def update_urgency(data, current_task):
        if current_task.importance == 1 and data["urgency"] == 1:
            data["eisehowers_id"] = 1
            return data["eisehowers_id"]
        if current_task.importance == 1 and data["urgency"] == 2:
            data["eisehowers_id"] = 2
            return data["eisehowers_id"]
        if current_task.importance == 2 and data["urgency"] == 1:
            data["eisehowers_id"] = 3
            return data["eisehowers_id"]
        if current_task.importance == 2 and data["urgency"] == 2:
            data["eisehowers_id"] = 4
            return data["eisehowers_id"]
        else:
            raise UpdateError



