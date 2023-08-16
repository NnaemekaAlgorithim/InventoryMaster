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
blueprint5 = Blueprint('records', __name__)

@blueprint5.route('/show_records', methods=['GET'])
@jwt_required()
def show_records():
    inventory, sales = []
    user_id = get_jwt_identity()
    inventory, sales = Inventory.show_all(user_id)
    inventory.to_dict()
    for record in inventory:
        inventory_list = record.to_dict()

    for record in sales:
        sales_list = record.to_dict()
