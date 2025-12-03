from accounting_app import app
from flask import jsonify, request
from datetime import datetime


# get user
# -> { "id": int, "name": string }
@app.route("/user/<user_id>", methods=[ "GET" ])
def user_get(user_id):
    pass

# delete user
@app.route("/user/<user_id>", methods=[ "DELETE" ])
def user_delete(user_id):
    pass

# create user
# <- { "name": string }
# -> { "id": int }
@app.route("/user", methods=[ "POST" ])
def user_create():
    pass

# list all users
# -> [ { "id": int } ]
@app.route("/users", methods=[ "GET" ])
def users_list():
    pass



# get category
# -> { "id": int, "name": string }
@app.route("/category/<category_id>", methods=[ "GET" ])
def category_get(category_id):
    pass

# delete category
@app.route("/category/<category_id>", methods=[ "DELETE" ])
def category_delete(category_id):
    pass

# create category
# <- { "name": string }
# -> { "id": int }
@app.route("/category", methods=[ "POST" ])
def category_create():
    pass

# list all categories
# -> [ { "id": int } ]
@app.route("/categories", methods=[ "POiGET" ])
def categories_list():
    pass



# get record
# -> { "id": int, "user_id": int, "category_id": int, "created_at": time, "amount": int }
@app.route("/record/<record_id>", methods=[ "GET" ])
def record_get(record_id):
    pass

# delete record
@app.route("/record/<record_id>", methods=[ "DELETE" ])
def record_delete(record_id):
    pass

# create record
# <- { "user_id": int, "category_id": int, "amount": int }
# -> { "id": int, "created_at": time }
@app.route("/record", methods=[ "POST" ])
def record_create(record_id):
    pass

# list all records matching filter
# <- ?user_id, ?category_id (category_id is optional)
# -> [ { "id": int } ]
@app.route("/record", methods=[ "GET" ])
def record_get_filter():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    pass


@app.route("/healthcheck")
def healthcheck():
    time = datetime.now()
    response = {
        "time": time,
        "status": "very good! !",
        "amogus": "healthy as usual",
    }
    return jsonify(response)
