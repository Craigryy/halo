### halo


halo is a book inventory api that uses flask python micro framework.
This API allows a user to create a book-category and add books to their categories.
The API allows user to interact only when authenticated,to ensured security .


![Screenshot (50)](https://github.com/Craigryy/halo/assets/116971272/a9580fb5-1356-416f-9106-c1429beddf86)



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

### Get all books


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


### Get a book


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


#USAGE Install dependencies using pip install -r requirements.txt
Run  python manager.py to start server
Test Api using POSTMAN or cURL

###UUSEAGE ON DOCKER 
Clone this repo into your local machine then run "docker-compose up --build" command on terminal inside cloned directory.
docker-compose up 
Open postman application and Test


####Database Used: 

Postgress.
Set User: postgres

Password: Favour98

Database name: halo
