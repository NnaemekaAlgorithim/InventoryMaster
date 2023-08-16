from flask import Flask, request, jsonify
from webflask.registration_and_login import blueprint1
from webflask.inventory_update import blueprint2
from webflask.sales_update import blueprint3
from webflask.delete_user import blueprint4
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import secrets
from flask_cors import CORS

app = Flask(__name__)

secret_key = secrets.token_hex(16)
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app)

# Register the blueprint with the app
app.register_blueprint(blueprint1)
app.register_blueprint(blueprint2)
app.register_blueprint(blueprint3)
app.register_blueprint(blueprint4)

if __name__ == '__main__':
    app.run()
