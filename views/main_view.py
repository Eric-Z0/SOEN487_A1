from flask import make_response, jsonify
from flask import Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@main_bp.route('/')
def soen487_a1():
    return jsonify({"title": "SOEN487 Assignment 1",
                    "student": {"id": "Your id#", "name": "Your name"}})
