from flask import Blueprint
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, request, jsonify
from models.users import User
from models.inventory import Inventory
from models.sales import Sales
from datetime import timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# Create a Blueprint instance
blueprint2 = Blueprint('stock_management', __name__)

@blueprint2.route('/new', methods=['POST'])
@jwt_required()
def new():
    data = request.get_json()
    name_of_product = data['name_of_product']
    number_in_stock = Decimal(data['number_in_stock'])
    price = data['price']
    user_id = get_jwt_identity()

    inventory = Inventory()

    try:
        # Check if the product already exists for the current user
        existing_inventory = Inventory.check_inventory(user_id, name_of_product)

        if existing_inventory:
            # Update the in_stock value by adding the new number_in_stock value
            existing_inventory.in_stock += number_in_stock
            json_inventory = existing_inventory.to_dict()
            existing_inventory.save()

            return jsonify(message='Update of old record successful', inventory=json_inventory), 200

        else:
            # Create a new Inventory object and populate its attributes
            inventory.user_id = user_id
            inventory.product_name = name_of_product
            inventory.in_stock = number_in_stock
            inventory.price = price

            # save inventory to the database
            inventory.save()
            json_inventory = inventory.to_dict()

            # Return a success message
            return jsonify(message='New inventory record added', inventory=json_inventory)

    except SQLAlchemyError as e:
        # Handle any potential database errors
        inventory.delete()
        inventory.save()
        return jsonify(message='Error updating inventory', error=str(e)), 500
