
# Poll System Backend - Poll Service

## Overview

The Poll Service is part of a microservices-based Poll System Backend.

It is responsible for managing polls, handling dynamic answer
options, processing user votes, and providing voting results.

The service communicates with the User Service through HTTP
requests to verify user registration before allowing users to vote.

The service is built using Python, FastAPI, and MySQL,
and runs inside a Docker container.


## Technologies Used

- Python
- FastAPI
- MySQL
- Docker
- Docker Compose
- Pydantic
- SQLAlchemy
- HTTPX
- Uvicorn
- Git and GitHub

## Architecture

The project follows a layered architecture that separates
responsibilities into different components.

- Controller: Handles incoming HTTP requests and responses.
- Service: Contains the business logic, voting rules,
  and communication with the User Service.
- Repository: Handles database operations.
- Schema: Defines and validates incoming data.
- Configuration: Manages application settings.
- Database: Manages the database connection.

The Poll Service maintains its own independent MySQL
database and communicates with the User Service through
HTTP requests.


## Features

- Create polls with dynamic answer options.
- Retrieve all polls.
- Retrieve a specific poll by ID.
- Update existing polls without recorded votes.
- Delete polls and their associated options and votes.
- Verify user registration through the User Service.
- Allow registered users to submit votes.
- Prevent duplicate votes within the same poll.
- Allow users to change or delete their votes.
- Retrieve vote counts for individual polls.
- Retrieve voting results for individual polls.
- Retrieve voting results across all polls.
- Retrieve a user's voting history.
- Remove all associated votes when a user is deleted.
- Validate poll questions and answer options.
- Prevent duplicate answer options.
- Store poll information in a dedicated MySQL database.


## Project Structure

```text
PythonProject12/
├── app/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── poll_controller.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── poll_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── poll_schema.py
│   │   └── vote_schema.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── poll_service.py
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── db-init/
│   ├── 01-polls.sql
│   ├── 02-poll-options.sql
│   └── 03-votes.sql
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```


## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Service home endpoint |
| GET | /polls | Retrieve all polls |
| GET | /polls/{poll_id} | Retrieve a specific poll |
| POST | /polls | Create a new poll |
| PUT | /polls/{poll_id} | Update an existing poll |
| DELETE | /polls/{poll_id} | Delete a poll and associated data |
| POST | /votes | Submit a vote |
| PUT | /votes/{user_id}/{poll_id} | Update an existing vote |
| DELETE | /votes/{user_id}/{poll_id} | Delete an existing vote |
| GET | /polls/{poll_id}/vote-count | Retrieve the total number of votes |
| GET | /polls/{poll_id}/results | Retrieve individual poll results |
| GET | /polls/results/all | Retrieve results across all polls |
| GET | /users/{user_id}/votes | Retrieve a user's voting history |
| DELETE | /users/{user_id}/votes | Delete all votes associated with a user |


## Database Structure

The Poll Service uses a dedicated MySQL database
called `poll_db`.

The database consists of three related tables:
`polls`, `poll_options`, and `votes`.

### Polls Table

| Column | Data Type | Description |
|---|---|---|
| poll_id | INT | Primary key, auto-incremented |
| question_title | VARCHAR(255) | Poll question |

### Poll Options Table

| Column | Data Type | Description |
|---|---|---|
| option_id | INT | Primary key, auto-incremented |
| poll_id | INT | Foreign key referencing the polls table |
| option_text | VARCHAR(255) | Answer option text |

### Votes Table

| Column | Data Type | Description |
|---|---|---|
| vote_id | INT | Primary key, auto-incremented |
| user_id | INT | ID of the user who submitted the vote |
| poll_id | INT | ID of the selected poll |
| option_id | INT | ID of the selected answer option |

All columns are defined as NOT NULL.


### Database Relationships and Constraints

- A poll can contain multiple answer options.
- Each answer option belongs to a specific poll.
- A poll can contain multiple votes from different users.
- Each user can submit only one vote per poll.
- Users can update their existing votes.
- A selected answer option must belong to the selected poll.
- Associated votes and answer options are removed
  when a poll is deleted.

The database uses primary keys, foreign keys,
and unique constraints to maintain data integrity.

The user_id column in the votes table is not a
foreign key to the User Service database.

User registration is verified through HTTP requests
to the User Service, maintaining separation between
the two microservices.

### Database Initialization

The database tables are initialized using the
following SQL scripts:

- `db-init/01-polls.sql`
- `db-init/02-poll-options.sql`
- `db-init/03-votes.sql`

These scripts are executed automatically by MySQL
when the Docker database is initialized with
a new database volume.


## Environment Variables

The application uses Pydantic BaseSettings to manage
configuration through environment variables.

| Variable | Default Value | Description |
|---|---|---|
| MYSQL_USER | root | MySQL username |
| MYSQL_HOST | 127.0.0.1 | MySQL server address |
| MYSQL_PORT | 3306 | MySQL server port |
| MYSQL_DATABASE | poll_db | Poll Service database name |
| MYSQL_PASSWORD | Required | MySQL database password |
| USER_SERVICE_URL | http://127.0.0.1:8000 | User Service address |

When running through Docker Compose, the database host
and service URL are overridden automatically.

The MYSQL_PASSWORD environment variable must be provided
before starting Docker Compose.

Database passwords should not be hardcoded or committed
to the GitHub repository.



## Installation and Setup

The Poll Service is part of the complete
Poll System Backend.

Both the User Service and Poll Service repositories
are required to run the complete application.

### Prerequisites

- Git
- Docker Desktop
- Docker Compose

### Running the Application

The Docker Compose configuration is located
in the User Service repository.

For complete installation, configuration,
and startup instructions, refer to the
[User Service README](https://github.com/eliorty13/-poll-system-user-service).

Both repositories must be located in the
same parent directory.

Docker Compose must be executed from the
User Service directory (PythonProject9).

Once the application is running, the Poll Service
can be accessed at:

- API: http://localhost:8001
- Swagger UI: http://localhost:8001/docs


## API Testing

The Poll Service API can be tested using
Swagger UI or Postman.


### Swagger UI

http://localhost:8001/docs

Swagger UI provides interactive API documentation
and allows developers to execute HTTP requests
directly from the browser.

### Postman

Base URL: http://localhost:8001

Postman can be used to send HTTP requests,
provide JSON request bodies, and inspect
response data and HTTP status codes.

### Main Testing Scenarios

- Create polls with dynamic answer options.
- Retrieve, update, and delete polls.
- Submit votes using registered users.
- Prevent unregistered users from voting.
- Prevent duplicate votes.
- Update and delete existing votes.
- Reject invalid answer options.
- Retrieve individual and overall poll results.
- Retrieve votes submitted by a specific user.
- Verify communication between both microservices.
- Verify associated vote removal when a user is deleted.

## Related Repositories

The Poll System Backend consists of two independent
microservices maintained in separate GitHub repositories.

- [User Service](https://github.com/eliorty13/-poll-system-user-service)
- [Poll Service](https://github.com/eliorty13/poll-system-poll-service)

Both services communicate through HTTP requests and
maintain their own independent MySQL databases.

The Docker Compose configuration is located in the
User Service repository and manages the complete system.
