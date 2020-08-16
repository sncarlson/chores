# Chores
The Chores API is a simple task management tool based on the concept of "chores" and "workers".
This project was created based on the needed the ability to track chore duration and frequency and the individual assigned.  

# Getting Started
Chores used the following as its tech stack:
* **Python 3** and **Flask**
* **SQLAlchemy ORM**
* **PostgreSQL**
* **Flask-Migrate**
* **Auth0** for authentication
* **unittest** for unit testing
* **Postman** for JWT testing

While I did use a virtual environment, it's not mandatory.

## Install Dependencies
To install requisite python packages:

`pip3 install -r requirements.txt`

## Setup Database
Setup and configure PostgreSQL in accordance with the guidance for your particular operating system.  Once configured, set an environment variable based on your database setup:

`export SQLALCHEMY_DATABASE_URI='postgres://replaceme:replaceme@localhost:5432/replaceme'`

## Run the Server
To start the development server, two additional environment variable need to be set.

Inside the `chores-backend` directory, start with the following commands:

```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```


# API Reference.

Base URL for development environment:

http://localhost:5000

```
## Endpoints
GET '/chores'
POST '/chores'
DELETE '/chores/<chore_id>'
PATCH '/chores/<chore_id>'

GET '/areas'
POST '/areas'
DELETE '/areas/<area_id>'
PATCH '/areas/<area_id>'

GET '/workers'
GET '/workers/<worker_id>'
POST '/workers'
DELETE '/workers/<worker_id>'
PATCH '/workers/<worker_id>

GET '/assigned-chores'
POST '/assigned-chores'
DELETE '/assigned-chores/<assigned_chore_id>'
PATCH '/assigned-chores/<assigned_chore_id>'

GET '/chores'
- Fetches an array of dictionary based chores available for assignment.
- Request Arguments: None
- Returns an array of dictionaries with chore information as follows:

{
  "chores": [
    {
      "area": "Kitchen",
      "cost": 0.5,
      "description": "Test Chore 1"
    },
    {
      "area": "Kitchen",
      "cost": 0.5,
      "description": "Test Chore 3"
    },
    {
      "area": "Lawn",
      "cost": 0.75,
      "description": "Test Chore 4"
    },
    {
      "area": "Bathroom",
      "cost": 0.76,
      "description": "Test Chore 5"
    }
  ],
  "success": true
}

POST '/chores'
- Adds a new chore
- Request Arguments: JSON body of description: Description of chore, cost: Value of chore, area: Area in which chore is completed.
- Returns success: true if complete and also the added chore with the applicable ID:

{
  "chore": {
    "area_id": 4,
    "cost": 0.75,
    "description": "Test Chore 10",
    "id": 10
  },
  "success": true
}

DELETE '/chores/<chore_id>'
- Deletes a chore
- Request Arguments: ID chore to delete
- Returns success: true if complete and ID of chore deleted.

{
  "delete": "10",
  "success": true
}



```


## Introduction
## Getting Started
### Base URL
### API Keys /Authentication (if applicable)
## Errors
### Response codes
### Messages
### Error types
## Resource endpoint library
### Organized by resource
### Include each endpoint
### Sample request
### Arguments including data types
### Response object including status codes and data types


# Deployment (if applicable)

# Authors

# Acknowledgements
