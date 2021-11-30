from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.categories_model import Categories
    from app.models.eisehowers_model import Eisehowers
    from app.models.task_model import Tasks
    from app.models.tasks_categories_model import TasksCategories