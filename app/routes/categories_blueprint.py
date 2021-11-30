from flask import Blueprint
from app.controllers.categories_controllers import create_category, patch_category, delete_category, get_all_categories
            
bp_categories = Blueprint("bp_categories", __name__)

bp_categories.post("/category")(create_category)
bp_categories.patch("/category/<int:id>")(patch_category)
bp_categories.delete("/category/<int:id>")(delete_category)
bp_categories.get("/")(get_all_categories)