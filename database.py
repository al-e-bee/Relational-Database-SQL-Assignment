# ===========================================================
# PART ONE: SET UP: Import necessary modules from SQLAlchemy
# ===========================================================
from sqlalchemy import create_engine, Integer, String, ForeignKey, Boolean, select, func, desc
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
    user_orders: Mapped[List['Order']] = relationship(back_populates='user', cascade='all, delete-orphan')
    
    # Clean printing of objects
    def __repr__(self):
        return f"<User(id={self.id}; name='{self.name}'; email='{self.email}')>"

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    
    # Relationship Product -> Order
    product_in_orders: Mapped[List['Order']] = relationship(back_populates='product')
    
    # Clean printing of objects
    def __repr__(self):
        return f"<Product(id={self.id}; name='{self.name}', price=${self.price})>"
    
class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer)
    # Add a 'status' column to the Order table (Boolean to represent shipped or not)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationship Orders -> User
    user: Mapped['User'] = relationship(back_populates='user_orders')
    product: Mapped['Product'] = relationship(back_populates='product_in_orders')
    
# ===========================
# PART THREE: Create Tables
# ===========================

# Automatically drop old tables for database refresh each run
Base.metadata.drop_all(engine)
# Creates tables fresh with each run
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

# ====================
# PART FIVE: Queries
# ====================

# Retrieve all users and print their info
all_users = session.execute(select(User)).scalars().all()
print(all_users)

# Retrieve all products and print their name and price
all_products = session.execute(select(Product)).scalars().all()
print(all_products)

# Retrieve all orders, showing the user's name, product name, and quantity
all_orders = session.execute(select(Order)).scalars().all()
for order in all_orders:
    order_user = order.user.name if order.user else "Unknown User"
    order_product = order.product.name if order.product else "Unknown Product"
    print(f"User: {order_user} | Product: {order_product} | Qty: {order.quantity}")

# Update a product's price
target_product_id = 1
query = select(Product).where(Product.id == target_product_id)
product = session.execute(query).scalars().first()
if product:
    product.price = 25
    session.commit()
    print(f"\nProduct ID: {product.id} | Product Name: {product.name}. The price for {product.name} has successfully been updated.")
else:
    # print("Product ID 1 not found for update.")
    print(f"Product ID {target_product_id} not found for update.")
    

# =================
# PART SIX: Bonus
# =================

# Add a 'status' column to the Order table (Boolean to represent shipped or not)
# ADDED IN ORDER TABLE CLASS #

# Update shipping status for an order
target_order_id = 3
query = select(Order).where(Order.id == target_order_id)
order = session.execute(query).scalars().first()
if order:
    order.status = True
    session.commit()
    # Check if the user relationship is available, otherwise fall back to a safe message
    user_name = order.user.name if order.user else "Unknown User"
    print(f"Order {target_order_id} for {user_name} has shipped!")
else:
    print(f"\nOrder ID {target_order_id} not found for update.")

# Query all orders that are not shipped
orders_not_shipped = session.execute(select(Order).where(Order.status == False)).scalars().all()
for order in orders_not_shipped:
    not_shipped_user = order.user.name if order.user else "Unknown User"
    print(f"Order: {order.id} for {not_shipped_user} has not shipped yet.")

# Count the total number of orders per user
# Select the user's name and count their orders
query = (
    select(User.name, func.count(Order.id).label('total_orders'))
    .join(Order) # Connect the Users to their orders
    .group_by(User.id) # Group the results by each individual user
    .order_by(desc('total_orders')) # Order by our count, highest to lowest
)

results = session.execute(query).all()
for row in results:
    print(f"User: {row.name} | Total Orders: {row.total_orders}")

# Delete a user by ID
target_user_id = 4
query = select(User).where(User.id == target_user_id)
user = session.execute(query).scalars().first()

if user:
    session.delete(user)
    session.commit()
    print(f'\nSuccessfully deleted user with ID {target_user_id} from the database.')
else:
    print(f"User {target_user_id} not found.")
    
