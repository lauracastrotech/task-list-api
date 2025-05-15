from flask import Blueprint, request, Response, abort, make_response
import requests
import os
from .route_utilities import validate_model, create_model
from ..models.goal import Goal
from ..models.task import Task
from ..db import db


bp=Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.get("")
def get_goals():
    query=db.select(Goal)
    goals = db.session.scalars(query.order_by(Goal.id))
    goals_response=[]
    for goal in goals:
        goals_response.append(goal.to_dict())
    return goals_response

@bp.get("/<id>")
def get_one_goals(id):
    goal = validate_model(Goal, id)
    return {"goal": goal.to_dict()},200 

@bp.get("/<goal_id>/tasks")
def get_one_goal_tasks(goal_id):
    goal = validate_model(Goal,goal_id)
    response_body = goal.to_dict()
    if "tasks" not in response_body:
        response_body["tasks"]=[]
    else:
        response_body["tasks"] = [task.to_dict() for task in goal.tasks]
    return response_body

@bp.post("")
def create_goal():
    request_body = request.get_json()
    response = create_model(Goal, request_body)
    return {"goal": response[0]}, response[1]

@bp.post("/<goal_id>/tasks")
def create_tasks_with_goal_id(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()
    tasks = request_body.get("task_ids",[])

    # This is my work around to get tests to pass. My concern is that this is a hardcoded solution that may cause side effects. Although I want to overwrite any existing tasks connected to the goal with teh given id, does this remove the task from the database? Technically tasks refers to a relationship of fields stored in a list, I'm not sure that this is the best solution.
    for task_id in goal.tasks:
        goal.tasks.remove(task_id)

    for task in tasks:
        valid_task = validate_model(Task, task)
        valid_task.goal_id = goal.id

    db.session.commit()

    return make_response({"id":goal.id, "task_ids":tasks},200)

@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    goal.title=request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

