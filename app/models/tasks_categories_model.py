# from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from app.models.categories_model import Categories
from app.models.task_model import Tasks
from dataclasses import dataclass


@dataclass
class TasksCategories(db.Model):
    id: int
    task_id: int
    category_id : int
   

    __tablename__ = "tasks_categories"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))  
    

    