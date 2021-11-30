from flask import Blueprint
from app.controllers.tasks_categories_controllers import get_taskcategories
            
bp_tasks_categories = Blueprint("bp_tasks_categories", __name__)

bp_tasks_categories.post("/")(get_taskcategories)