from accounting_app import app
from flask import jsonify, request
from datetime import datetime
import random



users = []
categories = []
records = []


# get user
# -> { "id": int, "name": string }
@app.route("/user/<user_id>", methods=[ "GET" ])
def user_get(user_id):
    global users

    print(users)

    user_id = int(user_id)
    user = next((user for user in users if user["id"] == user_id), None)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user["id"],
        "name": user["name"]
    }), 200


# delete user
@app.route("/user/<user_id>", methods=[ "DELETE" ])
def user_delete(user_id):
    global users

    old_len = len(users)
    users = [user for user in users if user["id"] != user_id]
    if old_len == len(users):
        return jsonify({
            "error": "User not found"
        }), 404

    return Response(status=204)

# create user
# <- { "name": string }
# -> { "id": int }
@app.route("/user", methods=[ "POST" ])
def user_create():
    global users

    data = request.get_json()
    if data is None:
        return jsonify({ "error": "No user name provided" }), 400

    id = random.getrandbits(64)

    users.append({
        "id": id,
        "name": data.get("name")
    })

    return jsonify({ "id": id }), 200

# list all users
# -> [ { "id": int } ]
@app.route("/users", methods=[ "GET" ])
def users_list():
    users_ids = [user["id"] for user in users]
    return jsonify(users_ids), 200



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
