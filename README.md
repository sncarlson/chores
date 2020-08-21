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

PATCH '/chores/<chore_id>'
- Updates a chore
- Request Arguments: ID chore to delete and update at least one of: description, cost, or area
- Returns success: true if complete and dictionary of chore with updated information.

{
  "chores": [
    {
      "area_id": 6,
      "cost": 0.76,
      "description": "Test Chore 4 Patch",
      "id": 4
    }
  ],
  "success": true
}

GET '/areas'
- Fetches an array of area dictionaries
- Request Arguments: None
- Returns success: Returns an array of dictionaries with area information as follows:

{
  "chores": [
    {
      "area": "Kitchen",
      "cost": 0.75,
      "description": "Test Chore 1"
    },
    {
      "area": "Garage",
      "cost": 1.75,
      "description": "Test Chore 2"
    },
    {
      "area": "Laundry Room",
      "cost": 1.85,
      "description": "Test Chore 3"
    }
  ],
  "success": true
}

POST '/areas'
- Creates an area
- Request Arguments: JSON body of name: name of area.
- Returns success: true if complete and area dictionary with id and name

{
  "area": {
    "id": 8,
    "name": "Test Area 1"
  },
  "success": true
}

DELETE '/areas/<area_id>'
- Deletes an area
- Request Arguments: ID area to delete
- Returns success: true if complete and ID of area deleted.

{
  "delete": "8",
  "success": true
}

PATCH '/areas/<area_id>'
- Updates an area
- Request Arguments: ID of area to delete
- Returns success: true if complete and dictionary of chore updated.

{
  "areas": [
    {
      "id": 6,
      "name": "Bedroom"
    }
  ],
  "success": true
}

GET '/workers'
- Fetches an array of worker dictionaries
- Request Arguments: None
- Returns success: Returns an array of dictionaries with worker information as follows:

{
  "success": true,
  "workers": [
    {
      "name": "Test Worker 1"
    },
    {
      "name": "Test Worker 2"
    },
    {
      "name": "Test Worker 3"
    }
  ]
}

GET '/workers/<worker_id>'
- Fetches an array of chores assigned to a particular worker
- Request Arguments: ID of worker
- Returns success: Returns an array of dictionaries with chore information for a particular worker as follows:

{
  "success": true,
  "workers": [
    {
      "chores": [
        {
          "area": "Laundry Room",
          "description": "Test Chore 3",
          "duration": "Two months",
          "frequency": "Every other day",
          "wage": 1.85
        },
        {
          "area": "Garage",
          "description": "Test Chore 2",
          "duration": "One Week",
          "frequency": "Twice a day",
          "wage": 1.75
        }
      ],
      "name": "Test Worker 2"
    }
  ]
}

POST '/workers'
- Creates a worker
- Request Arguments: JSON body of name: name of worker.
- Returns success: true if complete and worker dictionary with id and name

{
  "success": true,
  "worker": {
    "id": 1,
    "name": "Test Worker 1"
  }
}

DELETE '/workers/<worker_id>'
- Deletes a worker
- Request Arguments: ID of worker to delete
- Returns success: true if complete and ID of worker deleted.

{
  "delete": "4",
  "success": true
}

PATCH '/workers/<worker_id>
- Updates an area
- Request Arguments: ID of area to delete
- Returns success: true if complete and dictionary of chore updated.

{
  "success": true,
  "worker": [
    {
      "id": 3,
      "name": "Test Worker 3 Patch"
    }
  ]
}

GET '/assigned-chores'
- Fetches an array of assigned-chores dictionaries
- Request Arguments: None
- Returns success: Returns an array of dictionaries with worker information as follows:

{
  "assigned-chores": [
    {
      "area": "Bedroom",
      "chore": "Test Chore 4 Patch",
      "duration": "One month",
      "frequency": "Daily",
      "wage": 0.76,
      "worker": "Test Worker 3 Patch"
    },
    {
      "area": "Laundry Room",
      "chore": "Test Chore 3",
      "duration": "Two months",
      "frequency": "Every other day",
      "wage": 1.85,
      "worker": "Test Worker 2"
    },
    {
      "area": "Garage",
      "chore": "Test Chore 2",
      "duration": "One Week",
      "frequency": "Twice a day",
      "wage": 1.75,
      "worker": "Test Worker 2"
    }
  ],
  "success": true
}

POST '/assigned-chores'
- Creates an assigned-chore
- Request Arguments: JSON body of worker, chore, duration, and frequency
- Returns success: true if complete

{
  "success": true
}

DELETE '/assigned-chores/<assigned_chore_id>'
- Deletes an assigned-chore
- Request Arguments: ID of assigned-chore
- Returns success: true if complete and ID of worker deleted.

{
  "delete": "7",
  "success": true
}

PATCH '/assigned-chores/<assigned_chore_id>'
- Updates an assigned-chore
- Request Arguments: ID of assigned-chore to update.  Also, at least one of worker, chore, duration, or frequency
- Returns success: true if complete and dictionary of chore updated.

{
  "assigned-chore": [
    {
      "area": "Garage",
      "chore": "Test Chore 2",
      "duration": "Three years",
      "frequency": "Twice a Month",
      "wage": 1.75,
      "worker": "Test Worker 1"
    }
  ],
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
