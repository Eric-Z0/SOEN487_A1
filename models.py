from database import db


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


# an associate table associating client and ticket
booking_table = db.Table('booking',
                         db.Column('client_id', db.Integer, db.ForeignKey('person.id')),
                         db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.ticket_id')),
                         db.Column('quantity', db.Integer))


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    # 'Payment' is upper cased because we are looking for the class
    payments = db.relationship('Payment', backref='payer')
    bookings = db.relationship('Ticket', secondary=booking_table, backref='buyer', lazy='dynamic')

    def __repr__(self):
        return "<Person {}: {}>".format(self.id, self.name)


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.Text(), nullable=False)
    ticket_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Ticket {} {} {}>".format(self.ticket_id, self.movie_name, self.ticket_number)


class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    payment_amount = db.Column(db.Float, nullable=False)
    # 'person.id' is lower cased because we are looking for the table
    client_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    def __repr__(self):
        return "<Payment {}: {}>".format(self.client_id, self.payment_amount)
