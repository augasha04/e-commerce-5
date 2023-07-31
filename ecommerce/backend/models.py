from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from datetime import datetime
from sqlalchemy import column_property

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False, default="FirstName")
    second_name = db.Column(db.String, nullable=False, default="SecondName")
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String)
    password =db.Column(db.String(250), nullable=False)


    comment = db.relationship('Comment', backref='user')
    shopping_cart = db.relationship("Shopping_cart", back_populates='user')
     
    serialize_rules = ("-comment.user", "-shopping_cart.user")
   
    def to_dict(self):
        return {
             'id': self.id,
             'username': self.username,
             'first_name': self.first_name,
             'second_name': self.second_name,
             'date_of_birth': self.date_of_birth,
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
        else:
            return email
        
    
        
    @validates('email', 'username', 'first_name', 'second_name', 'date_of_birth', 'phone_number', 'address' )
    def validates_not_empty(self, key, value):
        if not value:
            raise ValueError(f"{key} cannot be empty")
        else:
            return value


class Comment(db.Model, SerializerMixin):
    __tablename__= "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    serialize_rules = ("-user.comment")

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'created_at': self.created_at,
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f'Comment: {self.comment}, ID: {self.id}'
    
eshop_products = db.Table('eshop_products',
    db.Column('eshop_id', db.Integer, db.ForeignKey('eshop.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)
    
class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(100))
    price = db.Column(db.Numeric)
    image_url = db.Column(db.String) 
    category = db.Column(db.String)
    stock = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=0)
    delivery_cost = db.Column(db.Integer)
    mb = db.Column(db.Float)
    cb = db.Column(db.Float)

    eshops = db.relationship('Eshop', secondary=eshop_products, back_populates='products')

    serialize_rules = ("-eshops.products", "-shopping_cart.product")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'stock': self.stock,
            'eshops': self.eshops,
            'mb': self.mb,
            'cb': self.cb
        }
    
    def __repr__(self):
        return f'Name: {self.name}, ID: {self.id}, Image: {self.image_url},'
    

class Eshop(db.Model, SerializerMixin):
    __tablename__ = "eshops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    logo_url = db.Column(db.String)
    address = db.Column(db.String, unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String, unique=True)

    products = db.relationship('Product', secondary=eshop_products, back_populates='eshops')
    
    serialize_rules = ("-products.eshops")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email,
            'products': self.products
        }
    
    def __repr__(self):
        return f'Name: {self.name}, ID: {self.id}'
    

class Shopping_cart(db.Model, SerializerMixin):
    __tablename__ = 'shopping_carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id =db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=0)


    user = db.relationship('User', back_populates='shopping_cart')
    product = db.relationship('Product')

    total = column_property(quantity * product.price)

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

class Order(db.Model,SerializerMixin):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id =db.Column(db.Integer, db.ForeignKey('products.id'))
    total = db.Column(db.Numeric)
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_address = db.Column(db.String, unique=True)
    payment_method = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method
        }
    
    def __repr__(self):
        return f'User: {self.user_id}, ID: {self.id}, Total: {self.total}'