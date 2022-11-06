from database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default='salao')
    active = Column(Boolean, nullable=False, default=True)
    password = Column(String(100), nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(String(20), nullable=False)
    type = Column(String(50), nullable=False, default='entry')

class Order(Base):
    __tablename__ = "orders"

    order_number = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String(100), nullable=False)
    date = Column(String(100), nullable=False)
    items = relationship("OrderItem")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(Integer, ForeignKey("orders.order_number"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product")
