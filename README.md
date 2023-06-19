# halo
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

category url data: id = category id

POST /categories/ | create a new category
Parameters/Input data: {"name":"name of category"}

GET /categories/ | List all the created categories in the database
Parameters/Input data: nil 

GET /categories/<int:id> | Get a single category in the database 
Parameters/Input data: nil 

PUT /categories/<int:id> | Update a category in the database
Parameters/Input data: {"name":"update a category name"}

DELETE /categories/<int:id> | Delete a category in the database 
Parameters/Input data: nil

BOOKMODEL url data:id = category id, bookmodel_id = bookmodel id

POST /categories/<int:id>/books/ | Create a new book in a category 
Parameters/Input data: {"name":"my categorybooks"}

PUT /categories/<int:id>/books/<int:books_id> | Update a bookmodel in a category
Parameters/Input data: {"name":"update my bookmodel"}

DELETE /categories/<int:id>/books/<int:books_id> | Delete a bookmodel in a category
Parameters/Input data: nil

##HOW TO USE 
login/registers via  POST auth/login route and is given a token
User uses token which expires after a period of 30 minutes.
User obtains token if he/she wants to continue using API services.
User uses token to make request to server for resources defined above.

##HOW TO USE TOKEN 
Upon auth/login a token is given 
Token should be used as header value with key 'Header'
Example :
Key:"x-access-token"
Value:<TOKEN>

if the key "x-aceess-token" isn't stated , an error message will appear.

RESTful API is STATELESS and so no user session is stored.


#USAGE Install dependencies using pip install -r requirements.txt
Run  python manager.py to start server
Test Api using POSTMAN or cURL

###UUSEAGE ON DOCKER 
Clone this repo into your local machine then run "docker-compose up --build" command on terminal inside cloned directory.
docker-compose up 
Open postman application and Test


####Database Used: Postgress.
Set User: postgres
Password: Favour98
Database name: halo
