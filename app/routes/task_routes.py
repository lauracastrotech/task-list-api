from flask import Blueprint, request, Response, abort, make_response
import requests
import os
from .route_utilities import validate_model, create_model
from datetime import datetime
from ..models.task import Task
from ..db import db

bp=Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    response = create_model(Task, request_body)
    return {"task": response[0]}, response[1]

@bp.get("")
def get_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")

    if sort_param == "asc":
        tasks = db.session.scalars(query.order_by(Task.title.asc()))
    elif sort_param == "desc":
        tasks = db.session.scalars(query.order_by(Task.title.desc()))
    else:
        tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = []
    for task in tasks:
        valid_task = task.to_dict()
        if not has_special_chars(valid_task["title"]):
            tasks_response.append(valid_task)
    return tasks_response

def has_special_chars(title):
    special_chars = "#$%()*+,-./:;<=>?@[\]^_`{|}~"
    for char in title:   
        if char in special_chars:
            raise ValueError
    return False

@bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return {"task": task.to_dict()},200 

@bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title=request_body["title"]
    task.description=request_body["description"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.patch("/<id>/mark_complete")
def mark_task_complete(id):
    task = validate_model(Task, id)

    data = {
            "token": f"{os.environ.get('SLACK_API_TOKEN')}",
            "channel":"test-slack-api",
            "text":"Someone just completed the task My Beautiful Task"
            }
    response = requests.post("https://slack.com/api/chat.postMessage", data=data, 
                                headers={
                                    "Authorization": f"Bearer {os.environ.get('SLACK_API_TOKEN')}"
                                })

    if not task.completed_at:
        task.completed_at = datetime.now()

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.patch("/<id>/mark_incomplete")
def mark_task_incomplete(id):
    task = validate_model(Task, id)

    if task.completed_at:
        task.completed_at = None

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")



