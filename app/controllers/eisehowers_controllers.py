from flask import request, current_app, jsonify
from app.models.eisehowers_model import Eisehowers
      
def create_eisehowers():
    data = request.get_json()
    result= Eisehowers(**data)


    current_app.db.session.add(result)
    current_app.db.session.commit()

    return jsonify(result)

def get_eisehowers():
    ...

def patch_eisehowers():
    ...

def delete_eisehowers():
    ...