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
blueprint3 = Blueprint('sale_management', __name__)

@blueprint3.route('/sale', methods=['POST'])
@jwt_required()
def sale():
    data = request.get_json()
    user_id = get_jwt_identity()
    product_name = data['name_of_product']
    product_price = Decimal(data['price_of_product'])
    quantity_sold = Decimal(data['quantity_sold'])

    try:
        # Check if the product exists in inventory
        existing_inventory = Inventory.check_inventory(user_id, product_name)

        if existing_inventory:
            # Check if in_stock is zero or less than quantity_sold
            remaining_stock = existing_inventory.in_stock

            if remaining_stock >= quantity_sold:
                # Update the inventory by reducing the quantity_sold
                existing_inventory.in_stock -= quantity_sold
                existing_inventory.save()
                json_inventory = existing_inventory.to_dict()

                # Create a new sale object using the Sales class
                sale = Sales(
                    user_id=user_id,
                    productInv_name=product_name,
                    product_price=product_price,
                    qty_sold=quantity_sold
                )

                # Save the sale object to the database
                sale.save()
                json_sale = sale.to_dict()

                return jsonify(message='Sale recorded successfully!', sale=json_sale, inventory=json_inventory), 200
            else:
                return jsonify(message='Insufficient stock for the sale'), 200
        else:
            return jsonify(message='Product is not in inventory'), 200

    except SQLAlchemyError as e:
        sale.delete()
        sale.save()
        return jsonify(message='Error processing sale', error=str(e)), 500
