### halo


halo is a book inventory api that uses flask python micro framework.
This API allows a user to create a book-category and add books to their categories
The API allows user to interact only when authenticated,to ensured security .

.![Screenshot (116)](https://github.com/Craigryy/halo/assets/116971272/5c8f1946-01e4-4c99-b1e8-9cc91bdd6de8)


##RESOURCES 

AUTH url_data:username = "username"

POST /auth/login | Logs a user in
Parameters/Input data: {"username":"createuser"}

User url data: username = username

Only visible/exposed on login

GET user/username
Parameters/Input data: nil

## Base URL

The base URL for all API endpoints is: `http://127.0.0.1:5000/`

## Authentication

The API requires authentication using an API key token . Include the API key in the  `Headers` of each request.

## HOW TO USE TOKEN :


Upon auth/login a token is given .
Token should be used as header value with key 'x-access-token'
Example :

Key: "x-access-token"


Value: {int:TOKEN}


## Endpoints

### Get all categories


GET /categories


Retrieves a list of all book categories in the inventory.


#### Response

- Status Code: 200 OK
- Content Type: application/json

Example Response:
json
[
    {
        "id": 1,
        "name": "Book 1",
        "created_by": "Author 1"
    },
    {
        "id": 2,
        "title": "Book 2",
        "created_by": "Author 2"
    }
]


### Get a category


GET /categories/{int:id}

Retrieves details of a specific book category by its ID.

#### Parameters

- `{id}` (integer, required): ID of the book.

#### Response

- Status Code: 200 OK
- Content Type: application/json

Example Response:
json
{
    "id": 1,
    "name": "Book 1",
    "created_by": "Author 1"
}


### Add a category


POST /categories


Adds a new book category to the inventory.

#### Request

- Content Type: application/json

Example Request Body:
json
{
    "name": "New Book",
    "created_by": "New User"
}


#### Response

- Status Code: 201 Created
- Content Type: application/json

Example Response:
json
{
    "id": 3,
    "name": "New Book",
    "created_by": "New Nmae"
}


### Update a category


PUT /categories/{int:id}


Updates the details of a specific book category by its ID.

#### Parameters

- `{id}` (integer, required): ID of the book category .

#### Request

- Content Type: application/json

Example Request Body:
json
{
    "name": "Updated Category",
    "created_by": "Updated name"
}


#### Response

- Status Code: 200 OK
- Content Type: application/json

Example Response:
json
{
    "id": 3,
    "name": "Updated category",
    "created_by": "Updated name "
}


### Delete a category 


DELETE /categories/{int:id}


Deletes a specific book by its ID.

#### Parameters

- `{id}` (integer, required): ID of the book category.

#### Response

- Status Code: 204 No Content

## Error Handling

If an error occurs, the API will respond with an appropriate error message and status code. Error responses will be in the following format:

json
{
    "error": {
        "code": 404,
        "message": "Book not found"
    }
}



### Add a book


POST /categories/<int:id>/books


Adds a new book into a category.

#### Request

- Content Type: application/json

Example Request Body:
json
{
    "title": "New Book",
    "author": "New Author"
}


#### Response

- Status Code: 201 Created
- Content Type: application/json

Example Response:
json
{
    "id": 3,
    "title": "New Book",
    "author": "New Author"
}


### Update a book

PUT /categories/{int:id}/books/<int:books_id>

Updates the details of a specific book in a category by its ID.

#### Parameters

- `{id}` (integer, required): ID of the book category .

- `{book_id}` (integer, required): ID of the book .


#### Request

- Content Type: application/json

Example Request Body:
json
{
    "name": "Updated Book",
    "author": "Updated Author"
}


#### Response

- Status Code: 200 OK
- Content Type: application/json

Example Response:
json
{
    "id": 3,
    "name": "Updated Book",
    "author": "Updated Author"
}


### Delete a book


DELETE /categories/{int:id}/books/{int:book_id}


Deletes a specific book by its ID.

#### Parameters

- `{id}` (integer, required): ID of the book category.

- `{book_id}` (integer, required): ID of the book .

#### Response

- Status Code: 204 No Content

## Error Handling

If an error occurs, the API will respond with an appropriate error message and status code. Error responses will be in the following format:

json
{
    "error": {
        "code": 404,
        "message": "Book not found"
    }
}



if the key "x-aceess-token" isn't stated , an error message will appear.

RESTful API is STATELESS and so no user session is stored.


### USEAGE ON HOW TO USE SWAGGER UI :

To access the Swagger UI and view your API documentation, follow these steps:

Start the Flask application: In your terminal or command prompt, navigate to the project directory containing the app.py file and execute the following command:

`python manager.py`

This will start the Flask application, and you should see output indicating that the application is running.

Open a web browser: Launch a web browser of your choice.

Access the Swagger UI: In the address bar of your web browser, enter the following URL:

http://localhost:5000/api/docs
This URL assumes that the Flask application is running on the default development server, listening on port 5000. If you're using a different port or domain, modify the URL accordingly.

Explore the Swagger UI: The Swagger UI interface should now be displayed in your web browser. You can browse through the available routes, view their parameters, and even test them directly from the Swagger UI.

### USAGE :

Install dependencies using pip install -r requirements.txt
Run `python manager.py` to start the server
Test API using POSTMAN or cURL

### USAGE ON DOCKER:

1. Clone this repository into your local machine.
2. Run the following command in the terminal within the cloned directory:
3. Open the Postman application or use cURL to test the API.

#### Database Used:

- Database: PostgreSQL
- User: postgres
- Password: Favour98
- Database name: halo

### Install dependencies using pip and npm:

``make install-dependencies``


### RUN THE FLASK_APP :

``make run-dev``

### Run the frontend development server (React):

``make run-frontend-dev``

### Usage with Docker:

1. Clone this repository and navigate to the project directory.
2. Build and run the application using Docker Compose:

``make run-docker``


### Database:

- Database: PostgreSQL
2. User: postgres
3. Password: Favour98
4. Database name: halo


### Makefile Tasks:

- install-dependencies: Install Python and frontend dependencies.
- run-dev: Run the Flask app locally for development.
- run-frontend-dev: Run the frontend locally for development.
- run-docker: Build and run the app using Docker Compose.
- deploy-heroku: Deploy the app to Heroku.
- clean: Clean up temporary files.
- help: Show available tasks.


For example, to install dependencies, run:
`
```make install-dependencies``
