from flask import Blueprint
from app.controllers.task_controllers import create_task, delete_task, patch_task
            
bp_task = Blueprint("bp_task", __name__)

bp_task.post("/task")(create_task)
bp_task.delete("/task/<id>")(delete_task)
bp_task.patch("/task/<id>")(patch_task)