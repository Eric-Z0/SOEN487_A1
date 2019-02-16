from flask import jsonify, make_response, request
import sqlalchemy
import models
from flask import Blueprint
ticket_bp = Blueprint('ticket', __name__)


@ticket_bp.route("/ticket")
def get_all_tickets():
    ticket_list = models.Ticket.query.all()
    return jsonify([models.row2dict(ticket) for ticket in ticket_list])


@ticket_bp.route("/ticket/<ticket_id>")
def get_ticket(ticket_id):
    # id is a primary key, so we'll have max 1 result row
    ticket = models.Ticket.query.filter_by(ticket_id=ticket_id).first()
    if ticket:
        return jsonify(models.row2dict(ticket))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this ticket id."}), 404)


@ticket_bp.route("/ticket", methods={"PUT"})
def create_ticket():
    # get the movie name first, if no movie name then fail
    movie_name = request.form.get("movie_name")
    ticket_number = request.form.get("ticket_number")
    if not movie_name or not ticket_number:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put ticket. Missing mandatory fields."}), 403)

    # check if the ticket with the given movie has existed
    ticket = models.Ticket.query.filter_by(movie_name=movie_name).first()
    if ticket:
        return make_response(jsonify({"code": 403,
                                      "msg": "Ticket with this movie name has existed"}), 403)
    else:
        ticket = models.Ticket(movie_name=movie_name, ticket_number=ticket_number)

    models.db.session.add(ticket)

    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot create ticket. "
        print(ticket_bp.config.get("DEBUG"))
        if ticket_bp.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


@ticket_bp.route("/ticket/update", methods={"PUT"})
def update_ticket():
    # get the movie name first, if no movie name then fail
    movie_name = request.form.get("movie_name")
    ticket_number = request.form.get("ticket_number")
    if not movie_name or not ticket_number:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot update ticket. Missing mandatory fields."}), 403)

    ticket_id = request.form.get("ticket_id")
    if not ticket_id:
        ticket = models.Ticket.query.filter_by(movie_name=movie_name).first()
    else:
        ticket = models.Ticket.query.filter_by(ticket_id=ticket_id).first()

    ticket.movie_name = movie_name
    ticket.ticket_number = ticket_number

    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot update ticket. "
        print(ticket_bp.config.get("DEBUG"))
        if ticket_bp.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


@ticket_bp.route("/ticket/delete", methods={"PUT"})
def delete_ticket():
    # id is a primary key, so we'll have max 1 result row
    ticket_id = request.form.get("ticket_id")
    ticket = models.Ticket.query.filter_by(ticket_id=ticket_id).first()
    if ticket:
        models.db.session.delete(ticket)
        try:
            models.db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot delete ticket. "
            print(ticket_bp.config.get("DEBUG"))
            if ticket_bp.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "ticket is successfully deleted"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this ticket id."}), 404)

