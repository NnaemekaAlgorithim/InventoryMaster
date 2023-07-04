from flask import Blueprint
from flask import Flask, request, jsonify
from models.users_record_update import User
from models.inventory_record_update import Inventory
from models.sales_record_update import Sales
from datetime import timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


# Create a Blueprint instance
blueprint1 = Blueprint('users', __name__)

@blueprint1.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    # Create a new User object and populate its attributes
    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = password

    # Save the user to the database
    user.save()

    # Return a success message
    return jsonify(message='Registration sucessful')


@blueprint1.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate inputs
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    # Retrieve user from the database
    user = User.retrive(email, password)

    if user:
        # Successful login
        access_token = create_access_token(identity = user.id)
        response = jsonify({'message': 'Login successful.', 'access_token': access_token})
        return response, 200
    else:
        # Invalid credentials
        return jsonify({'error': 'Invalid email or password.'}), 401
