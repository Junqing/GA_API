# GA_API

Template for FastAPI setup

This template contains 4 endspoints to handle fibonacci numbers:

- GET /fibonacci/{x}
  Fetches a fibonacci number by it's chonological order in the fibonacci sequence
- GET /fibonacci/sequence/{x}
  Fetches a chronologically ordered sequence of x in length
- POST /fibonacci/blacklist/{x}
  Input a number to be blacklisted and not shown in the above 2 endpoints
- DELETE /fibonacci/blacklist/undo/{x}
  Deletes the number from the blacklist

# Running the application

## Local run

Run command
$uvicorn app.main:app --reload
Access the application at 127.0.0.1:8000/docs or 127.0.0.1:8000/redoc

## Dockerized

Run command
$docker build -t myimage .
$docker run -d --name mycontainer -p 80:80 myimage
Access the application at http://localhost/docs
