import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Person
# from models import Person, db as tested_db

tested_app.config.from_object(TestConfig)


class TestPerson(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Person(id=1, name="Alice"))
        self.db.session.add(Person(id=2, name="Bob"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Person.query.delete()
        self.db.session.commit()

    def test_get_all_person(self):
        # send the request and check the response status code
        response = self.app.get("/person")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(person_list), list)
        self.assertDictEqual(person_list[0], {"id": "1", "name": "Alice"})
        self.assertDictEqual(person_list[1], {"id": "2", "name": "Bob"})

    def test_get_person_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/person/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(person, {"id": "1", "name": "Alice"})

    def test_get_person_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/person/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this person id."})

    def test_put_person_without_id(self):
        # do we really need to check counts?
        initial_count = Person.query.filter_by(name="Amy").count()

        # send the request and check the response status code
        response = self.app.put("/person", data={"name": "Amy"})
        self.assertEqual(response.status_code, 200)
        # print(response.status_code)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Person.query.filter_by(name="Amy").count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_person_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/person", data={"id": 3, "name": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        person = Person.query.filter_by(id=3).first()
        self.assertEqual(person.name, "Amy")
