# API_Project

Ongoing personal project building a test Flask based REST API.  This is just a project for learning and knowledge 
development. App currently only built with development and testing environment in mind.  New features are being added
regularly.

API has the following features:
- Client Creation
- A crude OAuth style authentication system with refresh tokens
- Simple POST and GET endpoints for creating and retrieving data in MongoDB
- Simple POST and GET endpoints for creating and retrieving data in Redis
- Endpoints to upload and download files to and from AWS S3 using base64 encoding

The Oauth system is just a simple implementation of the concept.  It is not secure and is not intended to be used in
production environments.  Client IDs and Client Secrets are stored encrypted in the database.  Refresh tokens are 
generated against a client id and secret and stored in redis for 15 minutes, after which they expire and a new token
must be generated.

To Install:

Simply clone the repo and use the docker-compose.yml file to build the app.  You will require docker to be installed on
your machine.  Once the app is built, you can use the postman collection to test the API.  The postman collection 
currently has all the features the API supports.  You may need to tweak local network and docker settings to be able to 
make calls to the API from postman.

Structure: 
- /app: Contains the main app code.
- /logs: Directory where logs are stored by default
- /postman: Contains the postman collection and environment files
- /docs: Directory for storing files temporarily while moving them between S3 and the end user.
