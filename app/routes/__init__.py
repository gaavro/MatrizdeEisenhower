

from flask import Flask

def init_app(app: Flask):
    from app.routes.categories_blueprint import bp_categories
    from app.routes.eisehowers_blueprint import bp_eisehowers
    from app.routes.task_blueprint import bp_task
    from app.routes.tasks_categories_blueprint import bp_tasks_categories

    app.register_blueprint(bp_categories)
    app.register_blueprint(bp_eisehowers)
    app.register_blueprint(bp_tasks_categories)
    app.register_blueprint(bp_task)