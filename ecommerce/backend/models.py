from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_file_name.db'  # Replace with your database URI
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
            raise ValueError("Enter a valid email")
        elif not email:
            raise ValueError(f'{email} cannot be empty')
        else:
            return email

    @validates('username', 'first_name', 'second_name', 'date_of_birth', 'phone_number', 'address')
    def validates_not_empty(self, key, value):
        if not value:
            raise ValueError(f"{key} cannot be empty")
        else:
            return value


class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    serialize_rules = ("-user.comment")

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'product_id': self.product_id

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

    serialize_rules = ("-products.eshops", "-products_info.eshop")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email,
            'products': [product.to_dict() for product in self.products]
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
    product = db.relationship('Product')

    @hybrid_property
    def total(self):
        return self.quantity * self.eshop_product_info.price

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
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
            'product_id': self.eshop_product_info.product_id,
            'product_name': self.eshop_product_info.product.name,
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
    product = db.relationship('Product', back_populates='eshops_info')

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
