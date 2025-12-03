from accounting_app import app
from flask import jsonify, request, Response
from datetime import datetime
import random

from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy(app)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)

    records = db.relationship("RecordModel", back_populates="user", lazy="dynamic")
    categories = db.relationship("CategoryModel", back_populates="user", lazy="dynamic")




class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    name = fields.Str(required=True)

class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    user = db.relationship("UserModel", back_populates="categories")
    records = db.relationship("RecordModel", back_populates="category", lazy="dynamic")




class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    amount = fields.Int(required=True)

class RecordModel(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=False,
        nullable=False,
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        unique=False,
        nullable=False,
    )

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    amount = db.Column(db.Integer, unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="records")
    category = db.relationship("CategoryModel", back_populates="records")


with app.app_context():
    print("CREATE DB")
    db.create_all()


categories = []
records = []


# get user
# -> { "id": int, "name": string }
@app.route("/user/<user_id>", methods=[ "GET" ])
def user_get(user_id):
    user_id = int(user_id)
    user = UserModel.query.get(user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "name": user.name
    }), 200


# delete user
@app.route("/user/<user_id>", methods=[ "DELETE" ])
def user_delete(user_id):
    user_id = int(user_id)
    user = UserModel.query.get(user_id)
    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    db.session.delete(user)
    db.session.commit()

    return Response(status=204)

# create user
# <- { "name": string }
# -> { "id": int }
@app.route("/user", methods=[ "POST" ])
def user_create():
    data = request.get_json()
    if data is None:
        return jsonify({ "error": "No user name provided" }), 400

    user = UserModel(name=data.get("name"))
    db.session.add(user)
    db.session.commit()

    return jsonify({ "id": user.id }), 200

# list all users
# -> [ { "id": int } ]
@app.route("/users", methods=[ "GET" ])
def users_list():
    users_ids = [user.id for user in UserModel.query.with_entities(UserModel.id).all()]
    return jsonify(users_ids), 200



# get category
# -> { "id": int, "name": string }
@app.route("/category/<category_id>", methods=[ "GET" ])
def category_get(category_id):
    global categories

    category_id = int(category_id)
    category = next((category for category in categories if category["id"] == category_id), None)

    if category is None:
        return jsonify({
            "error": "Category not found"
        }), 404

    return jsonify({
        "id": category["id"],
        "name": category["name"]
    }), 200

# delete category
@app.route("/category/<category_id>", methods=[ "DELETE" ])
def category_delete(category_id):
    global categories

    category_id = int(category_id)
    old_len = len(categories)
    categories = [category for category in categories if category["id"] != category_id]
    if old_len == len(categories):
        return jsonify({
            "error": "Category not found"
        }), 404

    return Response(status=204)

# create category
# <- { "name": string }
# -> { "id": int }
@app.route("/category", methods=[ "POST" ])
def category_create():
    global categories

    data = request.get_json()
    if data is None:
        return jsonify({ "error": "No category name provided" }), 400

    id = random.getrandbits(64)

    categories.append({
        "id": id,
        "name": data.get("name")
    })

    return jsonify({ "id": id }), 200

# list all categories
# -> [ { "id": int } ]
@app.route("/categories", methods=[ "GET" ])
def categories_list():
    global categories

    categories_ids = [category["id"] for category in categories]
    return jsonify(categories_ids), 200



# get record
# -> { "id": int, "user_id": int, "category_id": int, "created_at": time, "amount": int }
@app.route("/record/<record_id>", methods=[ "GET" ])
def record_get(record_id):
    global records

    record_id = int(record_id)
    record = next((record for record in records if record["id"] == record_id), None)

    if record is None:
        return jsonify({
            "error": "Record not found"
        }), 404

    return jsonify({
        "id": record["id"],
        "user_id": record["user_id"],
        "category_id": record["category_id"],
        "created_at": record["created_at"],
        "amount": record["amount"],
    }), 200

# delete record
@app.route("/record/<record_id>", methods=[ "DELETE" ])
def record_delete(record_id):
    global records

    record_id = int(record_id)
    old_len = len(records)
    records = [record for record in records if record["id"] != record_id]
    if old_len == len(records):
        return jsonify({
            "error": "Record not found"
        }), 404

    return Response(status=204)

# create record
# <- { "user_id": int, "category_id": int, "amount": int }
# -> { "id": int, "created_at": time }
@app.route("/record", methods=[ "POST" ])
def record_create():
    global records

    data = request.get_json()
    if data is None:
        return jsonify({ "error": "No record information provided" }), 400

    id = random.getrandbits(64)
    stamp = datetime.now()

    records.append({
        "id": id,
        "user_id": data.get("user_id"),
        "category_id": data.get("category_id"),
        "created_at": stamp,
        "amount": data.get("amount"),
    })

    return jsonify({ "id": id, "created_at": stamp }), 200

# list all records matching filter
# <- ?user_id, ?category_id (category_id is optional)
# -> [ { "id": int } ]
@app.route("/record", methods=[ "GET" ])
def record_get_filter():
    global records

    user_id = request.args.get("user_id")
    user_id = int(user_id) if (user_id is not None and user_id != "") else None

    category_id = request.args.get("category_id")
    category_id = int(category_id) if (category_id is not None and category_id != "") else None

    if user_id is None:
        return jsonify({ "error": "Can't list records without a user provided" }), 400

    records_filtered = [ record["id"] for record in records if record["user_id"] == user_id and (category_id is None or record["category_id"] == category_id) ]
    return jsonify(records_filtered), 200


@app.route("/healthcheck")
def healthcheck():
    time = datetime.now()
    response = {
        "time": time,
        "status": "very good! !",
        "amogus": "healthy as usual",
    }
    return jsonify(response)
