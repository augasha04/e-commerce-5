# server/app.py
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, EshopProductInfo, Comment, bcrypt
from flask_cors import CORS
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = b'm{\xf9\xec\xa0\xa7Gv\x98\x06\xa9\xfb\xdb\xe2\x8d\x86'

CORS(app)

api = Api(app)
db.init_app(app)
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


@app.route('/signup/user', methods=['POST'])
def signup_user():
  if request.method == 'POST':
      username = request.form['username']
      first_name = request.form['first_name']
      second_name = request.form['second_name']
      email = request.form['email']
      phone_number = request.form['phone_number']
      address = request.form['address']
      password = request.form['password']

      user_data=User(username=username,
                      first_name=first_name,
                      second_name=second_name,
                      email=email,
                      phone_number=phone_number,
                      address=address,
                      password=password)

      try:
          db.session.add(user_data)
          db.session.commit()
          return "User added. User id={}".format(user_data.id)
      except Exception as e:
          return(str(e))

@app.route('/signup/eshop', methods=['POST'])
def signup_eshop():
  if request.method == 'POST':
      name=request.form['name']
      logo_url=request.form['logo_url']
      address=request.form['address']
      phone_number=request.form['phone_number']
      email=request.form['email']

      eshop_data=Eshop(name=name,
                       logo_url=logo_url,
                       address=address,
                       phone_number=phone_number,
                       email=email)

      try:
          db.session.add(eshop_data)
          db.session.commit()
          return "Eshop added. Eshop id={}".format(eshop_data.id)
      except Exception as e:
          return(str(e))

@app.route('/products', methods=['GET', 'POST'])
def get_products():
    if request.method == 'GET':
        products_info = EshopProductInfo.query.order_by(EshopProductInfo.price.asc()).all()
        product_list = [product_info.to_dict() for product_info in products_info]
        response = make_response(jsonify(product_list), 200)
        return response
    elif request.method == 'POST':
        data = request.get_json()

        new_product = EshopProductInfo(
            name=data.get('name'),
            image_url=data.get('image_url'),
            category=data.get('category'),
            stock=data.get('stock'),
            rating=0,
            price=data.get('price'),
            delivery_cost=data.get('delivery_cost')
        )

        db.session.add(new_product)
        db.session.commit()

        return make_response(
            jsonify({"message": "You have successfully added a new product"}),
            201
        )


@app.route('/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_operations(product_id):
    product_info = EshopProductInfo.query.get(product_id)
    if not product_info:
        return jsonify({'message': 'Product not found'}), 404

    if request.method == 'GET':
        response_data = {
            'product': product_info.to_dict(),
            'comments': [comment.to_dict() for comment in product_info.comments]
        }
        return jsonify(response_data), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid data format'}), 400

        product_info.name = data.get('name', product_info.name)
        product_info.image_url = data.get('image_url', product_info.image_url)
        product_info.category = data.get('category', product_info.category)
        product_info.stock = data.get('stock', product_info.stock)
        product_info.price = data.get('price', product_info.price)
        product_info.delivery_cost = data.get('delivery_cost', product_info.delivery_cost)

        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200

    if request.method == 'DELETE':
        db.session.delete(product_info)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200

    return jsonify({'message': 'Method not allowed'}), 405


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
