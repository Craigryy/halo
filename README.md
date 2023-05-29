# halo
halo is a book inventory api that uses flask python micro framework.
This API allows a user to create a book-category and add books to their categories.
The API allows user to interact only when authenticated,to ensured security .



![Screenshot (50)](https://github.com/Craigryy/halo/assets/116971272/a9580fb5-1356-416f-9106-c1429beddf86)

`##RESOURCES`


`*** POST /user | create a User***`
Parameter : {"name":"james","password":"12345"}

A token is generated upon login, which is use to perform various task in which token is required.The token has an expiration time of 30mins .Token is only visible/exposed on login.


POST /auth/login | login a User
Parameter : {"name":"james","password":"12345"}


GET user/username
Parameters/Input data: nil

BOOK-CATEGORY url data: id = bookcategory id

POST /categories/ | create a new category
Parameters/Input data: {"name":"name of category","created_by":"who created the category"}

GET /categories/ | List all categories
Parameters/Input data: no parameter is needed to perform this task

GET /categories/<int:id> | Get single category
Parameters/Input data: id

PUT /categories/<int:id> | Update a category
Parameters : {"name":"update category name","created_by":"Have a nice day"}

DELETE /categories/<int:id> | Delete this single bucket list
Parameters/Input data: id

Book-Mpdel url data:id = bucketlist id, item_id = item id

POST /categories/<int:id>/books/ | Create a new book in a category
Parameters: {"title":"My book", "author":"harrison james"}

PUT /categories/<int:id>/books/<int:book_id> | Update a book  in a category 
Parameters: {"title":"update my book", "author":"harrison james" }

DELETE /categories/<int:id>/books/<int:book_id> | Delete a book in a category 
Parameters/Input data: id , book_id 


#USAGE
Install dependencies using pip install -r requirements.txt

On windows 
Run  the following commands in your terminal
python
from app import app,User,db,BookModel,BookCategory 
app.app_context().push()
db.create_all()

Test Api using POSTMAN or cURL


On linux -

Run  the following commands in your terminal
python3
from app import app,User,db,BookModel,BookCategory 
app.app_context().push()
db.create_all()


Database in use Postgres .
 - POSTGRES_PASSWORD=Favour98
 - POSTGRES_USER=postgres
 - POSTGRES_DB=kittie

Deloyment
