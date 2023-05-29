# halo
halo is a book inventory api that uses flask python micro framework.
This API allows a user to create a book-category and add books to their categories.
The API allows user to interact only when authenticated,to ensured security .





![Screenshot (50)](https://github.com/Craigryy/halo/assets/116971272/a9580fb5-1356-416f-9106-c1429beddf86)

##RESOURCES

AUTH url_data:username = "username"

POST /auth/login | Logs a user in
Parameters/Input data: {"username":"testuser"}

User url data: username = username

Only visible/exposed on login

GET user/username
Parameters/Input data: nil

BUCKETLIST url data: id = bucketlist id

POST /bucketlists/ | create a new bucketlist
Parameters/Input data: {"name":"name of bucketlist"}

GET /bucketlists/ | List all the created bucket lists
Parameters/Input data: nil 

GET /bucketlists/id | Get single bucket list
Parameters/Input data: nil 

PUT /bucketlists/id | Update this bucket list
Parameters/Input data: {"name":"updata bucketlist name"}

DELETE /bucketlists/id | Delete this single bucket list
Parameters/Input data: nil

ITEMS url data:id = bucketlist id, item_id = item id

POST /bucketlists/id/items/ | Create a new item in bucket list
Parameters/Input data: {"name":"my bucketlistitem", "Done":false }

PUT /bucketlists/id/items/item_id | Update a bucket list item
Parameters/Input data: {"name":"update my bucketlistitem", "Done":true }

DELETE /bucketlists/id/items/item_id | Delete an item in a bucket list
Parameters/Input data: nil

##WORKFLOW User login/registers via  POST auth/login route and is given a token
User uses token which expires after a period of 24 hour.
User obtains token if he/she wants to continue using API services.
User uses token to make request to server for resources defined above.

RESTful API is STATELESS and so no user session is stored.

User can also search for bucketlist using search parameter q.
GET /bucketlists/q=create and  GET /bucketlists/q=game&limit=4&page=1

#USAGE Install dependencies using pip install -r requirements.txt
Run  python manager.py runserver to start server
Test Api using POSTMAN or cURL

####Database Used: Postgress.
Set User: Administrator
Password: administrator
Database name: bucketlist
