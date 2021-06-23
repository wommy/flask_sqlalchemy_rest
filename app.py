from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# todo class/model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    completed = db.Column(db.Boolean, default=False)
    def __init__(self, name, completed):
        self.name = name
        self.completed = completed

# todo schema
class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id','name','completed')
todo_schema = TodoSchema()
# products _schema = ProductSchema(many=True)

# log class/model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    published = db.Column(db.Boolean, default=True)
    # TODO default datetime.Now()
    createdAt = db.Column(db.DateTime)
    def __init__(self, name, published, createdAt):
        self.name = name
        self.published = published
        self.createdAt = createdAt

# log schema
class LogSchema(ma.Schema):
    class Meta:
        fields = ('id','name','published','createdAt')
log_schema = LogSchema()
# products _schema = ProductSchema(many=True)

# quantity class/model
class Quantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    qty = db.Column(db.Integer, default=0)
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty

# quantities schema
class QuantitySchema(ma.Schema):
    class Meta:
        fields = ('id','name','qty')
quantity_schema = QuantitySchema()
# products _schema = ProductSchema(many=True)

# productMaterialsDetails class/model
class PMDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey(Quantity.id))
    materialId = db.Column(db.Integer, db.ForeignKey(Quantity.id))
    # product_id = db.Column(db.Integer, db.ForeignKey('quantity.id'), nullable=False)
    # material_id = db.relationship('Quantity', backref=db.backref('product', lazy=True))
    def __init__(self, productId, materialId):
        self.productId = productId
        self.materialId = materialId

# productMaterialDetails schema
class PMDetailsSchema(ma.Schema):
    class Meta:
        fields = ('id','productId','materialId')
pmdetails_schema = PMDetailsSchema()
#products_schema = ProductSchema(many=True)

# populating database
# @app.route('/populate/', methods=['POST'])
# def app_quantity():
#     new_product = Quantity(name, qty)
#     db.session.add(new_product)
#     db.session.commit()
#     return quantity_schema.jsonify(new_product)

# creating a quantity
@app.route('/quantity/', methods=['POST'])
def app_quantity():
    name = request.json['name']
    qty = request.json['qty']
    new_product = Quantity(name, qty)
    db.session.add(new_product)
    db.session.commit()
    return quantity_schema.jsonify(new_product)

# create product
@app.route('/product', methods=['POST'])
def app_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

# get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# get single products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# update product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)


# run server
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
