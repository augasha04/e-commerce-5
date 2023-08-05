from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from faker import Faker
from sqlalchemy import func 
import random
from datetime import datetime
from models import db, User, Comment, Eshop, ShoppingCart, Order, EshopProductInfo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # Replace with your database URI
db.init_app(app)
bcrypt = Bcrypt(app)

# Your route definitions go here...
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(users=user_list)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    first_name = data.get("first_name")
    second_name = data.get("second_name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    address = data.get("address")
    password = data.get("password")

    if not username or not email or not phone_number or not password:
        return jsonify(message="Username, email, phone_number, and password are required"), 400

    # Check if the username or email is already in use
    if User.query.filter_by(username=username).first() is not None:
        return jsonify(message="Username already exists"), 409

    if User.query.filter_by(email=email).first() is not None:
        return jsonify(message="Email already exists"), 409

    # Create the new user and add it to the database
    new_user = User(
        username=username, first_name=first_name, second_name=second_name,
        email=email, phone_number=phone_number, address=address
    )
    new_user.set_password(password)  # Set the user's password using the Bcrypt method

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User created successfully", user=new_user.to_dict()), 201

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="User deleted successfully")
    else:
        return jsonify(message="User not found"), 404

@app.route("/comments", methods=["GET"])
def get_comments():
    comments = Comment.query.all()
    comment_list = [comment.to_dict() for comment in comments]
    return jsonify(comments=comment_list)

@app.route("/eshops", methods=["GET"])
def get_eshops():
    eshops = Eshop.query.all()
    eshop_list = [eshop.to_dict() for eshop in eshops]
    return jsonify(eshops=eshop_list)

if __name__ == '__main__':
    # Generate fake user data
    fake = Faker()

    # Create the tables before adding the fake data
    with app.app_context():
        db.create_all()

        # Add fake users
        for _ in range(50):
            # Generate fake user data
            username = fake.user_name()
            firstname = fake.first_name()
            secondname = fake.last_name()
            email = fake.email()
            phonenumber = fake.phone_number()
            address = fake.address()
            password = fake.password()

            user = User(
                username=username, first_name=firstname, second_name=secondname,
                email=email, phone_number=phonenumber, address=address, password=password
            )

            db.session.add(user)

        # Add fake eshops
        for _ in range(50):
            name = fake.company()
            address = fake.address()
            phone_number = fake.phone_number()
            email = fake.email()

            eshop = Eshop(name=name, address=address, phone_number=phone_number, email=email)

            db.session.add(eshop)

        db.session.commit()  # Commit the user and eshop data first before generating product info

        # ... Rest of the fake data generation ...

    app.run()
