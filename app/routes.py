from app import app
from flask import json
from app.response import *
from app.models import *


def form_response(data):
    response = app.response_class(
        response=json.dumps(data.serialize()),
        mimetype='application/json'
    )
    return response

# @app.route('/test')
# def test():
#     data = ListResponse(["Einz", "Zwei", "Drei"], 1, 1, 3, False, True)
#     return form_response(data)

@app.route('/register')
def register():
    return "Register Page"

@app.route('/login')
def login():
    return "Login Page"

@app.route('/logout')
def logout():
    return "Logout Page"


# – http://localhost:5000/user
# – http://localhost:5000/user/<user_id>
# – http://localhost:5000/user/<user_id>/posts
@app.route('/user')
def users():
    # return "User page"
    users = User.query.all()
    data = ListResponse(users, 1, 1, 3, False, True)
    return form_response(data)


@app.route('/user/<user_id>/')
def user(user_id):
    return "User id: {}".format(user_id)

@app.route('/user/<user_id>/posts')
def user_posts(user_id):
    return "Posts for User id {}".format(user_id)


# – http://localhost:5000/posts
# – http://localhost:5000/posts/<post_id>
# – http://localhost:5000/posts/<post_id>/statistics
@app.route('/posts')
def posts():
    return "Posts Page"

@app.route('/posts/<post_id>')
def post(post_id):
    return "Posts id {}".format(post_id)

@app.route('/posts/<post_id>/statistics')
def post_stats(post_id):
    return "Statistics for Post id {}".format(post_id)


# – http://localhost:5000/statistics
# – http://localhost:5000/statistics/<statistics_id>
@app.route('/statistics')
def statistics_all():
    return "Statistics Page"

@app.route('/statistics/<statistics_id>')
def statistics(statistics_id):
    return "Statistics id: {}".format(statistics_id)
