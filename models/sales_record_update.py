#!/usr/bin/env python3
#!/usr/bin/env python3
"""Defines the sales class."""
import models
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship class.


class Sales(BaseModel, Base):
    """Represents a sale record for the MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table sales.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store sales.
        user_id (sqlalchemy String): The sales user id.
        inventory_name_of_product (sqlalchemy String): The name of the product.
        number_sold (sqlalchemy Integer): The number of products sold.
        inventory_price (sqlalchemy Integer): The price of the product.
    """
    __tablename__ = "sales"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    inventory_name_of_product = Column(String(128), Foreignkey("inventory.name_of_product"), nullable=False)
    number_sold = Column(Integer, default=0)
    inventory_price = Column(Integer, Foreignkey("inventory.price"), default=0)
