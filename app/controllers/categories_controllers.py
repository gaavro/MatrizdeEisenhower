from flask import request, current_app, jsonify

from app.models.categories_model import Categories
import psycopg2

from app.models.tasks_categories_model import TasksCategories

def create_category():
    try:
        data = request.json
        category= Categories(**data)


        current_app.db.session.add(category)
        current_app.db.session.commit()

        return jsonify(category), 201
    except psycopg2.errors.UniqueViolation:
        return {'msg': 'Category already exists!'}, 409


def patch_category(id):
    category = Categories.query.filter(Categories.id==id).one_or_none()
    try:
        current= Categories.query.get(id)
        data = request.get_json()
        if current == None: 
            return{"msg": "Category not found"},404
        for key, value in data.items():
            setattr(current, key, value)
        current_app.db.session.add(current)
        current_app.db.session.commit()
        return {
        "id": category.id,
        "name": category.name,
        "description": category.description
        }, 200
    
    except psycopg2.errors.UniqueViolation:
        return {'msg': 'Category already exists!'}, 409

def delete_category(id):
    current= Categories.query.get(id)
    if current== None: 
        return{"message": "Categoria não encontrada"},404
    current_app.db.session.delete(current)
    current_app.db.session.commit()
    return "", 204


def get_all_categories():
    categories_list = Categories.query.all()

    return jsonify([{
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "tasks": [{
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "priority": task.eisehowers_classification.type
            } for task in category.result]
        } for category in categories_list]), 200