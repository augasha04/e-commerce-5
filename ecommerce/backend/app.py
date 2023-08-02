# server/app.py
from flask import Flask, jsonify, request, make_response, session, redirect, url_for
#from werkzeug.exceptions import HTTPException, NotFound
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db 
from flask_cors import CORS
from werkzeug.security import check_password_hash
from models import db, User,  Comment, bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# app.json_encoder = SerializerMixin.json_encoder
app.secret_key= b'm{\xf9\xec\xa0\xa7Gv\x98\x06\xa9\xfb\xdb\xe2\x8d\x86'

CORS(app)

api = Api(app)
db.init_app(app)
# instantiate Bcrypt with app instance
bcrypt.init_app(app)
migrate = Migrate(app, db)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return jsonify(user={"id": user.id, "username": user.username})
    else:
        return jsonify(message="Invalid email or password"), 401
    

# @app.route('/products', methods=['GET', 'POST'])
# def get_products():
#     if request.method == 'GET':    
#         products = Product.query.order_by(Product.price.asc()).all()
#         product_list = [product.to_dict() for product in products]
#         response = make_response(jsonify(product_list), 200)
#         return response
#     elif request.method == 'POST':
#         data=request.get_json()

#         new_product= Product(
#             name=data.get('name'),
#             description=data.get('description'),
#             image_url=data.get('image_url'),
#             category=data.get('category'),
#             stock=data.get('stock'),
#             rating=0
#         )

#         db.session.add(new_product)
#         db.session.commit()

#         return make_response(
#             jsonify({"message":"You have successfully added a new product"}),
#             201
#         ) 
    
# @app.route('/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
# def product_operations(product_id):
#     product = Product.query.get(product_id)
#     if not product:
#         return jsonify({'message': 'Product not found'}), 404

#     if request.method == 'GET':
#         response_data = {
#             'product': product.to_dict(),
#             'comments': [comment.to_dict() for comment in product.comment]
#         }
#         return jsonify(response_data), 200

#     if request.method == 'PUT':
#         data = request.get_json()
#         if not data:
#             return jsonify({'message': 'Invalid data format'}), 400

#         # Use data.get() with default values for optional fields
#         product.name = data.get('name', product.name)
#         product.image_url = data.get('image_url', product.image_url)
#         product.description = data.get('description', product.description)
#         product.category = data.get('category', product.category)
#         product.stock = data.get('stock', product.stock)
#         db.session.commit()
#         return jsonify({'message': 'Product updated successfully'}), 200

#     if request.method == 'DELETE':
#         db.session.delete(product)
#         db.session.commit()
#         return jsonify({'message': 'Product deleted successfully'}), 200

#     return jsonify({'message': 'Method not allowed'}), 405



if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run()