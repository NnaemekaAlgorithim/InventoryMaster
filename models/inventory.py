#!/usr/bin/env python3
"""Defines the inventory class."""
import models
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Query


class Inventory(BaseModel, Base):
    """Represents an Inventory for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table inventory.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store inventory.
        user_id (sqlalchemy String): The inventory's user id.
        name_of_product (sqlalchemy String): The name of the product.
        number_in_stock (sqlalchemy Integer): The current quantity of product.
        price (sqlalchemy Integer): The price of the product.
    """
    
    __tablename__ = "inventory"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    product_name = Column(String(128), nullable=False)
    in_stock = Column(Integer, default=0)
    price = Column(Integer, default=0)
