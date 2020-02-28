# shield_api
My solution for the SHIELD INTELLIGENCE API assignment
## Installation
In order to build and start the server, run:

`docker-compose up`

Everything should run out of the box. It was tested on Arch Linux, and Windows
10 (with a small amount of tinkering. I had to replace localhost with the given IP and run
`git config --global core.autocrlf false` before calling `git clone`). There are
two containers: first running PostgreSQL database and second running flask.

## Endpoints
All the API endpoints from Section 2.2 are implemented, and following HTTP
request methods and user privileges should be used:

| Endpoint                   | HTTP method     | Privileges |
| -------------              | :-------------: | -----:     |
| register                   | POST            | no         |
| login                      | POST            | no         |
| logout                     | POST            | user       |
| user                       | GET             | admin      |
| user/<user_id>             | GET             | admin      |
| user/<user_id>/posts       | GET             | user       |
| posts                      | GET             | user       |
| posts                      | POST            | user       |
| posts/<post_id>            | GET             | user       |
| posts/<post_id>            | PUT             | admin      |
| posts/<post_id>            | DELETE          | admin      |
| posts/<post_id>/statistics | GET             | user       |
| statistics                 | GET             | user       |
| statistics                 | POST            | user       |
| statistics/<statistics_id> | GET             | user       |
| statistics/<statistics_id> | PUT             | admin      |
| statistics/<statistics_id> | DELETE          | admin      |


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
In order to test the API, scripts from the `curl_scripts` directory can be used. 
For more information about the JSON format for the POST requests, please refer to
`curl_scripts/README.md`.

## Configuration
Environment variables for the database and the JWT are placed into the `.env` file.
