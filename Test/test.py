"""Script to test end points using HTTpretty python library. """

try:
    from flask_app import flask_app, db
    import unittest
    import httpretty
    import json
    import requests

except Exception as e:
    print("missing some modules".format(e))


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.test_client()
        self.ctx = flask_app.app_context()
        self.ctx.push()
        db.create_all()

        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_routes(self):
        httpretty.enable()
        json_body = json.dumps({'status': 'ok', 'value': '123'})
        httpretty.register_uri(httpretty.GET, 'http://example.com/',
                               body=json_body,
                               content_type='application/json',
                               status=200)
        response = requests.get('http://example.com/')
        print(response.status_code)

    def test_createuser(self):

        data_user = {'name': 'Harrison', 'password': 'James'}
        json_body = json.dumps(data_user)
        httpretty.register_uri(httpretty.POST, 'http://127.0.0.1:5000/auth/login',
                               body=json_body, content_type='application/json',
                               status=200)

        response = requests.post('http://127.0.0.1:5000/user')
        self.assertTrue(response.status_code == 200)


class bookmodelCase(APITestCase):

    def test_create_bookmodel(self):
        bookmodel = {'title': 'Harrison', 'author': 'James'}
        json_body = json.dumps(bookmodel)
        httpretty.register_uri(httpretty.POST, 'http://127.0.0.1:5000/<int:id>/categories/<int:book_id>',
                               body=json_body,
                               content_type='application/json',
                               status=200)

        response = requests.post('http://127.0.0.1:5000/<int:id>/categories/<int:book_id>')
        self.assertTrue(response.status_code == 200)

    def test_update_bookmodel(self):
        book_id = 1
        updated_book_data = {
            'title': 'John Doe',
            'author': 'Craigry'
        }

        # Register a mock response for the PUT request to update a user
        httpretty.register_uri(
            httpretty.PUT,
            f'http://127.0.0.1:5000/<int:id>/categories/{book_id}',
            body='{"message": "Book model updated successfully"}',
            content_type='application/json',
            status=200,
        )

        # Make a request to update the user
        response = requests.put(f'http://127.0.0.1:5000/<int:id>/categories/{book_id}', json=updated_book_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Perform assertions on the response data
        self.assertEqual(data['message'], 'Book model updated successfully')


class test_category(APITestCase):

    def test_create_userg(self):
        httpretty.enable()
        json_body = json.dumps({'status': 'ok', 'value': '123'})
        httpretty.register_uri(httpretty.GET, 'http://example.com/',
                               body=json_body,
                               content_type='application/json',
                               status=200)
        response = requests.get('http://example.com/')
        print(response.status_code)

    def test_delete_category(self):
        httpretty.enable()
        category_id = 1

        # Register a mock response for the DELETE request to delete a user
        httpretty.register_uri(
            httpretty.DELETE,
            f'http://example.com/categories/{category_id}',
            status=204,
        )

        # Make a request to delete the user
        response = requests.delete(f'http://example.com/categories/{category_id}')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
