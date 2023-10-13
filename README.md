# API_Project

Ongoing personal project building a test Flask based REST API.  App currently only built with development and testing 
environment in mind.  Currently, the API supports simple POST and GET requests to wrote and read from MongoDB and Redis.
It also uses localstack to simulate AWS s3.  You can upload and download files of various types from s3.  To upload,
You send a base64 encoded string.  When you make a download request for a file, it is returned to you also in a base64
encoded string.  More features are planned for the future.  

To Install:
Simply clone the repo and use the docker-compose.yml file to build the app.  You will require docker to be installed on
your machine.  Once the app is built, you can use the postman collection to test the API.  The postman collection 
currently has all the features the API supports.  You may need to tweak local network and docker settings to be able to 
make calls to the API from postman.

Structure:
/app: Contains the main app code.
/logs: Directory where logs are stored by default
/postman: Contains the postman collection and environment files

Unit Tests are planned one the API is more feature complete.