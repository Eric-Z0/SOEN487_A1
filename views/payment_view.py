from flask import jsonify, make_response, request
import sqlalchemy
import models
from flask import Blueprint
payment_bp = Blueprint('payment', __name__)


@payment_bp.route("/payment")
def get_all_payments():
    payment_list = models.Payment.query.all()
    return jsonify([models.row2dict(payment) for payment in payment_list])


@payment_bp.route("/payment/<payment_id>")
def get_payment(payment_id):
    # id is a primary key, so we'll have max 1 result row
    payment = models.Payment.query.filter_by(payment_id=payment_id).first()
    if payment:
        return jsonify(models.row2dict(payment))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this payment id."}), 404)


@payment_bp.route("/payment", methods={"PUT"})
def create_payment():
    # get the movie name first, if no movie name then fail
    amount = request.form.get("payment_amount")
    payer_id = request.form.get("client_id")
    if not amount or not payer_id:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot create payment. Missing mandatory fields."}), 403)

    payment = models.Payment(payment_amount=amount, client_id=payer_id)
    models.db.session.add(payment)

    try:
        models.db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot create payment. "
        print(payment_bp.config.get("DEBUG"))
        if payment_bp.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


@payment_bp.route("/payment/delete", methods={"PUT"})
def delete_payment():
    # id is a primary key, so we'll have max 1 result row
    payment_id = request.form.get("payment_id")
    payment = models.Payment.query.filter_by(payment_id=payment_id).first()

    if payment:
        models.db.session.delete(payment)
        try:
            models.db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot delete payment. "
            print(payment_bp.config.get("DEBUG"))
            if payment_bp.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "payment is successfully deleted"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this payment id."}), 404)



