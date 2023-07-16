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
blueprint4 = Blueprint('delete_user', __name__)

@blueprint4.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    user_id = get_jwt_identity()
    users = User()
    users.remove_user(user_id)
    users.save
    return jsonify(message='user deleted')
