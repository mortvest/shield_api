# shield_api
My solution for the SHIELD INTELLIGENCE API assignment
## Instructions
In order to build and start the server, run:

`docker-compose up`

everything should run out of the box (tested on a Arch Linux system). There are
two containers: first running the PostgreSQL database and second running flask.

## Token system
In order to implement the access restriction in a User/Group fashion, I have
used the flask-jwt token system. After sending credentials as JSON through the
POST method to `localhost:5000/login`, a JSON file in a format, specified in
Section 2.3 is returned, containing an access token. The system can deduce the
user privileges from the token. In order to access the restricted endpoints,
access token should be placed inside the HTTP header, using following format:

`Authorization: Bearer <TOKEN>`

The access token is revoked after sending a POST request to `localhost:5000/logout`


## Testing 
In order to test the API, scripts from the curs_scripts directory can be used. 
For more information about the JSON format for the POST, please refer the
README.md.
