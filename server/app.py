#!/usr/bin/env python3

# Import necessary libraries/modules for the Flask app
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

# Initialize the Flask app
app = Flask(__name__)

# Set up the SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# Disable modification tracking to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set json.compact to False for more readable JSON formatting
app.json.compact = False

# Set up Flask-Migrate with our Flask app and the database
migrate = Migrate(app, db)

# Initialize the database with the Flask app
db.init_app(app)

# Define the root route, which displays a welcome message
@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# Define a route to get all bakeries
@app.route('/bakeries')
def bakeries():
    # Create an empty list to store bakeries
    bakeries = []
    
    # Iterate over all bakeries in the database
    for bakery in Bakery.query.all():
        # Convert each bakery to a dictionary and add to our list
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'updated_at': bakery.updated_at
        }
        bakeries.append(bakery_dict)
        
    # Create a Flask response with our list of bakeries and a 200 status code
    response = make_response(jsonify(bakeries), 200)
    
    return response

# Define a route to get a bakery by its ID
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Fetch the bakery by its ID from the database
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    # Convert the bakery object to a dictionary
    bakery_dict = Bakery.to_dict(bakery)
    
    # Create a Flask response with the bakery's data and a 200 status code
    response = make_response(jsonify(bakery_dict), 200)
    # Explicitly set the response's content type to JSON
    response.headers["Content-Type"] = "application/json"    
    
    return response

# Define a route to get baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Fetch all baked goods and order them by price in descending order
    bakedGoods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # Convert each baked good to a dictionary and store in a list
    bakedGoods_list = [bg.to_dict() for bg in bakedGoods]
    
    return jsonify(bakedGoods_list)

# Define a route to get the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Fetch the most expensive baked good from the database
    expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    # Convert the baked good object to a dictionary
    expensive_baked_good_dict = expensive_baked_good.to_dict()
    
    return jsonify(expensive_baked_good_dict)

# Run the Flask app when this script is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
