from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from faker import Faker
from sqlalchemy import func 
import random
from faker import Faker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # Replace with your database URI
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False, default="FirstName")
    second_name = db.Column(db.String, nullable=False, default="SecondName")
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String)
    password = db.Column(db.String(250), nullable=False)

    comment = db.relationship('Comment', backref='user')
    shopping_cart = db.relationship("ShoppingCart", back_populates='user')

    serialize_rules = ("-comment.user", "-shopping_cart.user")

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address
        }

    def __repr__(self):
        return f'User: {self.username}, ID: {self.id}'

    @validates('email')
    def validates_email(self, key, email):
        if '@' not in email:
            raise ValueError("Email should contain '@'")
        elif not email:
            raise ValueError("Email cannot be empty")
        else:
            return email


class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    eshop_product_info_id = db.Column(db.Integer, db.ForeignKey('eshop_product_info.id'))

    serialize_rules = ("-user.comment",)

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'eshop_product_info_id': self.eshop_product_info_id
        }

    def __repr__(self):
        return f'Comment: {self.comment}, ID: {self.id}'


class Eshop(db.Model, SerializerMixin):
    __tablename__ = "eshops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    logo_url = db.Column(db.String)
    address = db.Column(db.String, unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String, unique=True)

    products_info = db.relationship('EshopProductInfo', back_populates='eshop')

    serialize_rules = ("-products_info.eshop",)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email,
            'eshop_product_info': [info.to_dict() for info in self.products_info]
        }

    def __repr__(self):
        return f'Name: {self.name}, ID: {self.id}'


class ShoppingCart(db.Model, SerializerMixin):
    __tablename__ = 'shopping_carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    eshop_product_info_id = db.Column(db.Integer, db.ForeignKey('eshop_product_info.id'))
    quantity = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='shopping_cart')

    @hybrid_property
    def total(self):
        return self.quantity * self.eshop_product_info.price

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'eshop_product_info': self.eshop_product_info.to_dict(),
            'quantity': self.quantity,
            'total': self.total
        }

    def __repr__(self):
        return f'Quantity: {self.quantity}, ID: {self.id}'


class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    eshop_product_info_id = db.Column(db.Integer, db.ForeignKey('eshop_product_info.id'))
    total = db.Column(db.Numeric)
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_address = db.Column(db.String)
    payment_method = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'eshop_product_info_id': self.eshop_product_info_id,
            'product_name': self.eshop_product_info.name,
            'price': self.eshop_product_info.price,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method
        }

    def __repr__(self):
        return f'User: {self.user_id}, ID: {self.id}, Total: {self.total}'


class EshopProductInfo(db.Model, SerializerMixin):
    __tablename__ = 'eshop_product_info'

    id = db.Column(db.Integer, primary_key=True)
    eshop_id = db.Column(db.Integer, db.ForeignKey('eshops.id'))
    name = db.Column(db.String)
    image_url = db.Column(db.String)
    category = db.Column(db.String)
    stock = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric)
    delivery_cost = db.Column(db.Numeric)

    eshop = db.relationship('Eshop', back_populates='products_info')

    def to_dict(self):
        return {
            'id': self.id,
            'eshop_id': self.eshop_id,
            'name': self.name,
            'image_url': self.image_url,
            'category': self.category,
            'stock': self.stock,
            'rating': self.rating,
            'price': self.price,
            'delivery_cost': self.delivery_cost,
        }
        if __name__ == '__main__':
            with app.app_context():
                db.create_all()
# Generate fake user data
fake = Faker()
# Create the tables before adding the fake data
with app.app_context():
    db.create_all()
    for _ in range(50):
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
    for _ in range(50):
        name = fake.company()
        address = fake.address()
        phone_number = fake.phone_number()
        email = fake.email()
        eshop = Eshop(name=name, address=address, phone_number=phone_number, email=email)
        db.session.add(eshop)
    db.session.commit()  # Commit the user and eshop data first before generating product info
    # Generate fake EshopProductInfo for each eshop individually
    for eshop in Eshop.query.all():
        for _ in range(50):
            name = fake.name()
            category = fake.word()
            stock = fake.random_int(min=0, max=100)
            rating = fake.random_int(min=0, max=5)
            price = fake.random_int(min=10, max=1000)
            deliverycost = fake.random_int(min=5, max=50)
            eshop_product_info = EshopProductInfo(
                eshop=eshop, name=name, category=category, stock=stock,
                rating=rating, price=price, delivery_cost=deliverycost
            )
            db.session.add(eshop_product_info)
    db.session.commit()  # Commit the EshopProductInfo data
    # Generate fake comments
    for _ in range(50):
        comment_text = fake.text(max_nb_chars=200)  # Generate random comment text
        created_at = fake.date_time_this_decade()  # Generate a random datetime within the current decade
        # Get a random user and eshop product from the database
        user = User.query.order_by(func.random()).first()
        eshop_product = EshopProductInfo.query.order_by(func.random()).first()
        # Check if user and eshop_product are not None
        if user is not None and eshop_product is not None:
            # Create the Comment object and add it to the session
            comment = Comment(
                comment=comment_text, created_at=created_at,
                user_id=user.id, eshop_product_info_id=eshop_product.id
            )
            db.session.add(comment)
    db.session.commit()  # Commit the comments data
    # Generate fake shopping carts
    for _ in range(50):
        # Get a random user and eshop product from the database
        user = User.query.order_by(func.random()).first()
        eshop_product = EshopProductInfo.query.order_by(func.random()).first()
        # Check if user and eshop_product are not None
        if user is not None and eshop_product is not None:
            # Generate a random quantity between 1 and 5
            quantity = random.randint(1, 5)
            # Create the ShoppingCart object and add it to the session
            shopping_cart = ShoppingCart(
                user_id=user.id, eshop_product_info_id=eshop_product.id, quantity=quantity
            )
            db.session.add(shopping_cart)
    db.session.commit()  # Commit the shopping carts data
    # Generate fake order data
with app.app_context():
    for _ in range(50):
        # Get a random user and eshop product from the database
        user = User.query.order_by(func.random()).first()
        eshop_product = EshopProductInfo.query.order_by(func.random()).first()
        # Check if user and eshop_product are not None
        if user is not None and eshop_product is not None:
            # Generate a random total between 10 and 1000
            total = random.randint(10, 1000)
            # Generate a random status from a list of options
            status_options = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
            status = random.choice(status_options)
            # Generate a random datetime within the current decade
            created_at = fake.date_time_this_decade()
            # Generate a random shipping address and payment method
            shipping_address = fake.address()
            payment_method = fake.credit_card_provider()
            # Create the Order object and add it to the session
            order = Order(
                user_id=user.id, eshop_product_info_id=eshop_product.id, total=total,
                status=status, created_at=created_at, shipping_address=shipping_address,
                payment_method=payment_method
            )
            db.session.add(order)
    # Commit the changes to the database
    db.session.commit()

    

