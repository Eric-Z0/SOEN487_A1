from flask import Flask
from config import TestConfig
from database import db

# need an app before we import models because models need it
app = Flask(__name__)
app.config.from_object(TestConfig)
db.app = app
db.init_app(app)

# db.create_all()
from views.main_view import main_bp
from views.person_view import person_bp
from views.ticket_view import ticket_bp
from views.payment_view import payment_bp
app.register_blueprint(main_bp)
app.register_blueprint(person_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(payment_bp)


if __name__ == '__main__':
    app.run()
