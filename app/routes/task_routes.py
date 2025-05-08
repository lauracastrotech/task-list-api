from flask import Blueprint, request, Response, abort, make_response
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..models.task import Task
from ..db import db

bp=Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_tasks():
    return get_models_with_filters(Task, request.args)
    '''
    From the response body, get an array of tasks. If the length of the response it zero, return []
    Otherwise, convert tasks to dictionary
    '''
# When there are no saved task, this should return []

@bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return {"task": task.to_dict()},200 

# @task_bp.get("/<id>")
# def get_one_task(id):
#     task = validate_model(Task, id)
#     return {"task": task.to_dict()}

# @bp.put("/<id>")
# def update_task(id):
#     task = validate_model(Task, id)
#     request_body = request.get_json()

#     task.title=request_body["title"]
#     task.description=request_body["description"]

#     db.session.commit()
#     return Response(status=204, mimetype="application/json")

# @bp.delete("/<id>")
# def delete_task(id):
#     task = validate_model(Task, id)
#     db.session.delete(task)
#     db.session.commit()
#     return Response(status=204, mimetype="application/json")

# @bp.get("?sort=asc")
# def get_asc_sorted_tasks():
    
#     pass3