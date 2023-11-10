## Jiseti Backend
Welcome to the backend repository of Jiseti, a platform designed to tackle corruption in Africa by allowing citizens to report incidents of corruption and request government intervention. This backend is built using FastAPI and SQLite to provide a robust and efficient foundation for the Jiseti project.

## Table of Contents
Getting Started
Installation
Usage
API Endpoints
Contributing
License
Getting Started
To get started with the Jiseti backend, follow the installation instructions below.

## Installation
Clone this repository to your local machine:

Navigate to the project directory:

Install the required dependencies using pip or pipenv

Run the FastAPI server:
uvicorn main:app --reload

## API Endpoints
Authentication
POST /api/token
Generate a JWT token for authentication.
Input: { "username": "your_username", "password": "your_password" }
User Management
POST /api/users/

Create a new user account.
Input: { "username": "new_user", "password": "new_password" }
GET /api/users/me

Get information about the currently authenticated user.
Red-Flag Records
POST /api/redflags/

Create a new red-flag record.
Input: { "title": "Corruption Incident", "description": "Details about the incident", "location": {"lat": 12.34, "lon": -56.78} }
GET /api/redflags/

Get a list of all red-flag records.
GET /api/redflags/{redflag_id}

Get details about a specific red-flag record.
PUT /api/redflags/{redflag_id}

Update details of a specific red-flag record.
DELETE /api/redflags/{redflag_id}

Delete a specific red-flag record.
Intervention Records
POST /api/interventions/

Create a new intervention record.
Input: { "title": "Government Intervention Request", "description": "Details about the request", "location": {"lat": 12.34, "lon": -56.78} }
GET /api/interventions/

Get a list of all intervention records.
GET /api/interventions/{intervention_id}

Get details about a specific intervention record.
PUT /api/interventions/{intervention_id}

Update details of a specific intervention record.
DELETE /api/interventions/{intervention_id}

Delete a specific intervention record.
Admin Actions
PUT /api/admin/change-status/{record_id}
Change the status of a record to either "under investigation," "rejected," or "resolved."

## License
This project is licensed under the MIT License.
