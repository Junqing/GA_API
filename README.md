# GA_API

Template for FastAPI setup

This template contains 4 endspoints to handle fibonacci numbers:

- GET /fibonacci/{x}
  - Fetches a fibonacci number by it's chonological order in the fibonacci sequence
- GET /fibonacci/sequence/{x}
  - Fetches a chronologically ordered sequence of x in length
- POST /fibonacci/blacklist/{x}
  - Input a number to be blacklisted and not shown in the above 2 endpoints
- DELETE /fibonacci/blacklist/undo/{x}
  - Deletes the number from the blacklist

# Running the application

## Local run

Run command

`$uvicorn app.main:app --reload`

Access the application at `127.0.0.1:8000/docs` or `127.0.0.1:8000/redoc`

## Dockerized

Run command

`$docker build -t myimage .`
`$docker run -d --name mycontainer -p 80:80 myimage`

Access the application at http://localhost/docs

## testing

Run command

`$pytest`

Will run through the tests defined in app.test_main.py file

## Features

- pytests for testing
- flake8 for linting
- fastapi_pagination for pagination support
- basic logging

## Features considered, not yet implemented

- ORM with db connection
- Schema contract to ensure output format
- Auth and functions for security
- AWS components, helper functions
  - X ray for logging monitoring
  - Secrets manager
