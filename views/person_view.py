from flask import jsonify, make_response, request
import sqlalchemy
import models
from flask import Blueprint
person_bp = Blueprint('person', __name__)


@person_bp.route("/person")
def get_all_person():
    person_list = models.Person.query.all()
    return jsonify([models.row2dict(person) for person in person_list])


@person_bp.route("/person/<person_id>")
def get_person(person_id):
    # id is a primary key, so we'll have max 1 result row
    person = models.Person.query.filter_by(id=person_id).first()
    if person:
        return jsonify(models.row2dict(person))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this person id."}), 404)


@person_bp.route("/person/delete/<person_id>", methods={"POST"})
def delete_person(person_id):
    # id is a primary key, so we'll have max 1 result row
    person = models.Person.query.filter_by(id=person_id).first()
    if person:
        models.db.session.delete(person)
        try:
            models.db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot put ticket. "
            print(person_bp.config.get("DEBUG"))
            if person_bp.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "person is successfully deleted"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this person id."}), 404)


@person_bp.route("/person", methods={"PUT"})
def put_person():
    # get the name first, if no name then fail
    name = request.form.get("name")
    if not name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put person. Missing mandatory fields."}), 403)
    person_id = request.form.get("id")
    if not person_id:
        p = models.Person(name=name)
    else:
        p = models.Person(id=person_id, name=name)

    models.db.session.add(p)
    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(person_bp.config.get("DEBUG"))
        if person_bp.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})
