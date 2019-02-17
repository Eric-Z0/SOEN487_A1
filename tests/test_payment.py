import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Payment, Person

tested_app.config.from_object(TestConfig)


class TestPayment(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Person(id=1, name="Alice"))
        self.db.session.add(Person(id=2, name="Bob"))
        self.db.session.add(Payment(payment_id=1, payment_amount=10.5, client_id=1))
        self.db.session.add(Payment(payment_id=2, payment_amount=12.5, client_id=2))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Payment.query.delete()
        Person.query.delete()
        self.db.session.commit()

    def test_get_all_payments(self):
        # send the request and check the response status code
        response = self.app.get("/payment")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        ticket_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(ticket_list), list)
        self.assertDictEqual(ticket_list[0], {"payment_id": "1", "payment_amount": "10.5", "client_id": "1"})
        self.assertDictEqual(ticket_list[1], {"payment_id": "2", "payment_amount": "12.5", "client_id": "2"})

    def test_get_payment_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/payment/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        payment = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(payment, {"payment_id": "1", "payment_amount": "10.5", "client_id": "1"})

    def test_get_payment_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/payment/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this payment id."})

    # Testing new payment insertion
    def test_create_payment_with_valid_clientId(self):

        # send the request and check the response status code
        response = self.app.put("/payment", data={"payment_amount": 7.2, "client_id": 2})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        payment = Payment.query.filter_by(payment_id=3).first()
        self.assertEqual(payment.payment_amount, 7.2)
        self.assertEqual(payment.client_id, 2)

        # Testing new payment insertion

    def test_create_payment_with_invalid_clientId(self):
        # send the request and check the response status code
        response = self.app.put("/payment", data={"payment_amount": 7.2, "client_id": 3})
        self.assertEqual(response.status_code, 404)

    def test_update_payment_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.put("/payment/update", data={"payment_id": 2, "payment_amount": 17.5, "client_id": 2})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        payment = Payment.query.filter_by(payment_id=2).first()
        self.assertEqual(payment.payment_amount, 17.5)

    def test_update_payment_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.put("/payment/update", data={"payment_id": 1000000, "payment_amount": 7.5, "client_id": 2})
        self.assertEqual(response.status_code, 404)

    def test_update_payment_with_invalid_clientId(self):
        # send the request and check the response status code
        response = self.app.put("/payment/update", data={"payment_id": 2, "payment_amount": 7.2, "client_id": 3})
        self.assertEqual(response.status_code, 404)

    # Testing exist payment deletion by id
    def test_delete_payment_with_valid_id(self):

        self.db.session.add(Person(id=3, name="Ellen"))
        self.db.session.commit()

        # send the request and check the response status code
        create_response = self.app.put("/payment", data={"payment_amount": 7.2, "client_id": 3})
        self.assertEqual(create_response.status_code, 200)

        payment = Payment.query.filter_by(payment_id=3).first()
        self.assertEqual(payment.payment_amount, 7.2)
        self.assertEqual(payment.client_id, 3)

        # send the request and check the response status code
        delete_response = self.app.put("/payment/delete", data={"payment_id": 3})
        self.assertEqual(delete_response.status_code, 200)

        payment = Payment.query.filter_by(payment_id=3).first()
        self.assertEqual(payment, None)

    # Testing non-exist payment deletion by id
    def test_delete_payment_with_invalid_id(self):
        # send the request and check the response status code
        delete_response = self.app.put("/payment/delete", data={"payment_id": 1000000})
        self.assertEqual(delete_response.status_code, 404)
