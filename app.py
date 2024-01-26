from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

CORS(app)

db = SQLAlchemy(app)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route('/')
def hello_world():
  return 'Hello World'

@app.route('/api/products', methods=["GET"])
def fetch_products():
   products_data = Product.query.all()
   products = []

   for product in products_data:
      item = {
         "id": product.id,
         "name": product.name,
         "price": product.price,
      }
      products.append(item)
   return products

@app.route('/api/products/add', methods=["POST"])
def add_product(): 
   data = request.json
   if 'name' in data and 'price' in data:
      product = Product(name = data["name"], price = data["price"], description = data.get("description", ""))
      db.session.add(product)
      db.session.commit()
      return jsonify({ 'message': 'Produto cadastrado com sucesso! 👌✨✨' }), 201
   return jsonify({ 'message': 'Invalid product data' }), 400

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
   product = Product.query.get(product_id)
   if product:
      return jsonify({
         "id": product.id,
         "name": product.name,
         "description": product.description
      }), 200
   return jsonify({ "message": "Product not found." }), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
   product = Product.query.get(product_id)
   if not product:
      return jsonify({ "message": "Product not found." }), 404
   
   data = request.json

   if 'name' in data:
      product.name = data['name']
   if 'price' in data:
      product.price = data['price']
   if 'description' in data:
      product.description = data['description']
   
   db.session.commit()
   return jsonify({}), 204

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
   product = Product.query.get(product_id)
   if product:
      db.session.delete(product)
      db.session.commit()

      return jsonify(), 204
   return jsonify({ 'message': 'Product not found.' }), 404

if __name__ == "__main__":
  app.run(debug=True)

