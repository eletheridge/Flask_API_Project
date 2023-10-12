# API_Project

Ongoing project building a test Flask based RESTful API.

Can be run locally using included docker and docker-compose.  It will spin up A MongoDB container, a Redis Container, a localstack container, and the app.
Currently, the API only supports simple read and write of entries to both MongoDB and Redis servers.  You can start up the entire stack and use CURL or Postman to test.

The localstack service is currently unused, but is planned to be used to demonstate interacting with an S3 bucket.

The service will also be expanded to represent a microservice structure with more than one container interacting with each other via internal APIs.
