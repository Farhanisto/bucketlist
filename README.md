# bucketlist
a Bucket List is a list of things that one has not done before but wants to do before dying.

Installation and Setup

Clone the repo

https://github.com/Farhanisto/bucketlist.git
Navigate to the root folder

cd bucketlist
create a virtualenv

virtualenv --python=python3 venv
activate virtualenv and export the environment variables by running the following

Install the requirements

pip install -r requirements.txt
Create the main and the test database from the command line by running the script:

$ createdb bucketlist
$ createdb developbucketlist
$ createdb testbucketlist

Initialize, migrate, upgrade the datatbase

python manage.py db init
python manage.py db migrate
python manage.py db upgrade
Launch the progam

Run

python manage.py runserver
Interact with the API, send http requests using Postman or alternatively use the swagger documentation to test it

API Endpoints

URL Endpoint	HTTP Methods	Summary
/auth/register/	POST	Register a new user
/auth/login/	POST	Login and retrieve token
/auth/status/   POST get notified of weather a token is expired or not
/auth/logout/   POST logout
/bucketlists/	POST	Create a new Bucketlist
/bucketlists/	GET	Retrieve all bucketlists for user
/bucketlists/?page=1&per_page=3/	GET	Retrieve three bucketlists per page
/bucketlists/?q=name/	GET	searches a bucketlist by the name
/bucketlists/<id>/	GET	Retrieve a bucketlist by ID
/bucketlists/<id>/	PUT	Update a bucketlist
/bucketlists/<id>/	DELETE	Delete a bucketlist
/bucketlists/<id>/items/	POST	Create items in a bucketlist
/bucketlists/<id>/items/<item_id>/	DELETE	Delete an item in a bucketlist
/bucketlists/<id>/items/<item_id>/	PUT	update a bucketlist item details
Testing

You can run the tests

python manage.py test

To test with coverage run
python manage.py cov


