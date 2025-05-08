from flask import Blueprint, request, Response, abort, make_response
import requests
import os
from .route_utilities import validate_model, create_model
from ..models.goal import Goal
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

@bp.post("")
def create_goal():
    request_body = request.get_json()
    response = create_model(Goal, request_body)
    return {"goal": response[0]}, response[1]

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