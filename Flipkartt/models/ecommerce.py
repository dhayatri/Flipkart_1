from utils.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    wishlist = db.relationship('Wishlist', back_populates='user', lazy='dynamic')
    cart = db.relationship('Cart', back_populates='user', lazy='dynamic')


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    desc = db.Column(db.String(1000), nullable=True)
    category = db.Column(db.String(100), nullable=False)

    wishlist_items = db.relationship('Wishlist', back_populates='product', lazy='dynamic')
    cart_items = db.relationship('Cart', back_populates='product', lazy='dynamic')


class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    user = db.relationship('User', back_populates='wishlist')
    product = db.relationship('Product', back_populates='wishlist_items')


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', back_populates='cart')
    product = db.relationship('Product', back_populates='cart_items')
