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
    
# ===========================
# PART THREE: Create Tables
# ===========================

Base.metadata.create_all(engine)  

# ========================
# PART FOUR: Insert Data
# ========================

# Create Users
user_ali = User(name='Ali', email='a_baker@email.com')
user_matt = User(name='Matt', email='baker_m@email.com')

# Create Products
shirt = Product(name='shirt', price=20)
shoes = Product(name='shoes', price=50)
tablet = Product(name='tablet', price=500)
headphones = Product(name='headphones', price=200)


# Create Orders
order1 = Order(user=user_ali, product=shirt, quantity=2)
order2 = Order(user=user_ali, product=shoes, quantity=1)
order3 = Order(user=user_matt, product=tablet, quantity=1)
order4 = Order(user=user_matt, product=headphones, quantity=1)

# Commit the data
session.add_all([user_ali, user_matt, shirt, shoes, tablet, headphones, order1, order2, order3, order4])

session.commit()

