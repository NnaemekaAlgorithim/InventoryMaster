from flask import Flask, request, jsonify, session
from models.users_record_update import User
from datetime import timedelta
import secrets

app = Flask(__name__)

# Set the permanent session lifetime to 120 minutes
app.permanent_session_lifetime = timedelta(minutes=120)

secret_key = secrets.token_hex(16)

app.secret_key = secret_key

@app.route('/register', methods=['POST'])
def register_user():
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

    # Return a success message or any other desired response
    return jsonify(message='Registration sucessful')

@app.route('/login', methods=['POST'])
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
        session['status'] = user.id
        return jsonify({'message': 'Login successful.'}), 200
    else:
        # Invalid credentials

        return jsonify({'error': 'Invalid email or password.'}), 401


if __name__ == '__main__':
    app.run()
