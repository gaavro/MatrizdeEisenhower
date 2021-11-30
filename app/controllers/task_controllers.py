from flask import request, current_app, jsonify
from app.exceptions.exceptions import InvalidImportanceOrUrgencyError, UpdateError
from app.models.categories_model import Categories
from app.models.eisehowers_model import Eisehowers
from app.models.task_model import Tasks
from app.models.tasks_categories_model import TasksCategories
import psycopg2

def create_task():
    data = request.json
    categories = []

    try:
        Tasks.classify_eisenhower(data)
        for category in data["categories"]:
            if Categories.query.filter(category["name"]==Categories.name).first() == None:
                current_app.db.session.add(Categories(name=category["name"]))
                current_app.db.session.commit()
            categories.append(Categories.query.filter(category["name"]==Categories.name).first())
        del data["categories"]

        new_task = Tasks(**data)
        current_app.db.session.add(new_task)
        current_app.db.session.commit()

        for category in categories:
            current_app.db.session.add(TasksCategories(task_id=new_task.id, category_id=category.id))
            current_app.db.session.commit()


        filtered_categories = []
        for category in new_task.categories:
            filtered_categories.append(Categories.query.filter(Categories.id==category.id).first())

        return {
            "id": new_task.id,
            "name": new_task.name,
            "description": new_task.description,
            "duration": new_task.duration   ,
            "eisehowers_classification": new_task.eisehowers_classification.type,
            "categories": [{"nome": category.name} for category in filtered_categories]
        }, 201


    except InvalidImportanceOrUrgencyError as e:
        return e.message, 404
    except psycopg2.errors.UniqueViolation:
        return {'msg': 'Task already exists!'}, 409


def patch_task(id):
    try:
        current_task = Tasks.query.get(id)
        data = request.json
        data["eisenhower_id"] = 1

        if current_task == None:
            return {"msg": "Task not found"}, 404

        for key, value in data.items():
            if key == "urgency":
                Tasks.update_urgency(data, current_task)
            if key == "importance":
                Tasks.update_importance(data, current_task)
            setattr(current_task, key, value)


        current_app.db.session.add(current_task)
        current_app.db.session.commit()


        return {
                "id": current_task.id,
                "name": current_task.name,
                "description": current_task.description,
                "duration": current_task.duration,
                "eisenhower_classification": current_task.eisehowers_classification.type
            }, 200


    except UpdateError:
        return {"msg": "Valores inválidos"}, 404




def delete_task(id):
    current_task= Tasks.query.get(id)
    if current_task == None: 
        return{"message": "Task não encontrada"},404
    current_app.db.session.delete(current_task)
    current_app.db.session.commit()
    return "", 204