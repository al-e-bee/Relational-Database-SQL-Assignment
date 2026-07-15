# ===========================================================
# PART ONE: SET UP: Import necessary modules from SQLAlchemy
# ===========================================================
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapped_column, Mapped
from typing import List

# Create an engine and base:
engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# ========================
# PART TWO: Define Tables
# ========================

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Relationship User -> Order
    user_orders: Mapped[List['Order']] = relationship(back_populates='user')

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    
    # Relationship Product -> Order
    product_in_orders: Mapped[List['Order']] = relationship(back_populates='product')
    
class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer)

    # Relationship Orders -> User
    user: Mapped['User'] = relationship(back_populates='user_orders')
    product: Mapped['Product'] = relationship(back_populates='product_in_orders')
    
   