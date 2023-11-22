# Flask_API_Project

This is an ongoing "for fun" project.  This is a simple Flask based API that interacts with MongoDB,
Redis, and AWS S3 (localstack).  The intention is a microservice style setup that runs in docker containers.
Currently, there is a main app container for the main API endpoints, an Auth service container with endpoints for 
validating client credentials and generating auth tokens.  There is also a MongoDB container, a Redis container, and
a localstack container for S3.  The app build is completely orchestrated using docker-compose.

The app runs on a uWSGI server and is served by nginx (Though nginx is not enabled for development work)

## API has the following features:
- Client Creation
- A crude OAuth style authentication system with auth tokens
- Simple POST and GET endpoints for creating and retrieving data in MongoDB
- Simple POST and GET endpoints for creating and retrieving data in Redis
- Endpoints to upload and download files to and from AWS S3 using base64 encoding

## To Install:

Simply clone the repo and use the docker-compose.yml file to build the app.  You will require docker to be installed on
your machine.  Once the app is built, you can use the postman collection to test the API.  The postman collection 
currently has all the features the API supports.  You may need to tweak local network and docker settings to be able to 
make calls to the API from postman.

## Structure:
- /app: Contains the main API app
- /auth_svc: Contains the Auth service API app
- /common: Contains common code used by both the main API and Auth service
- /Postman: Contains a postman collection for testing the API


*Future plans are to add more services to the app.*
