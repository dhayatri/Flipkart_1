from flask import Flask, render_template, request, redirect, flash, url_for
from utils.db import db
from models.ecommerce import *
import uuid


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
flask_app.secret_key = 'your_secret_key'

@flask_app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@flask_app.route('/about')
def about():
    return render_template('about.html')

@flask_app.route('/groceries')
def groceries():
    products = Product.query.all()
    return render_template('groceries.html', products=products)


@flask_app.route('/mobiles')
def mobiles():
    products = Product.query.all()
    return render_template('mobiles.html', products=products)

@flask_app.route('/fashions')
def fashions():
    products = Product.query.all()
    return render_template('fashions.html', products=products)

@flask_app.route('/home-furniture')
def home_furniture():
    products = Product.query.all()
    return render_template('home_furniture.html', products=products)

@flask_app.route('/electronics')
def electronics():
    products = Product.query.all()
    return render_template('electronics.html', products=products)

@flask_app.route('/appliences')
def appliences():
    products = Product.query.all()
    return render_template('appliences.html', products=products)


@flask_app.route('/add-product')
def add_product():
    return render_template('add_product.html')


# wish list and cart
@flask_app.route('/wishlist')
def wishlist():
    wishlist_items = Wishlist.query.all()
    return render_template('wishlist.html', wishlist=wishlist_items)


@flask_app.route('/cart')
def cart():
    cart_items = Cart.query.all()
    print(f"cart_items: {cart_items}")
    # total = sum(item.quantity * item.price for item in cart_items)
    return render_template('cart.html', cart=cart_items)


@flask_app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = 1

    product = Product.query.get(product_id)
    print(f"product: {product}")
    if not product:
        flash('Product not found.')
        return redirect(url_for('home'))

    cart_item = Cart.query.filter_by(product_id=product.id).first()
    print(f"cart_item: {cart_item}")
    if cart_item:
        cart_item.quantity += quantity
    else:
        new_cart_item = Cart(user_id=1, product_id=product.id, quantity=quantity)
        db.session.add(new_cart_item)

    db.session.commit()
    flash(f'Added {product.name} to cart.')
    return redirect(url_for('index'))


@flask_app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    cart_item = Cart.query.filter_by(product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.')
    else:
        flash('Item not found in cart.')

    return redirect(url_for('cart'))


@flask_app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    product_id = request.form.get('product_id')

    product = Product.query.get(product_id)
    print(f"product: {product}")
    if not product:
        flash('Product not found.')
        return redirect(url_for('home'))

    wishlist_item = Wishlist.query.filter_by(product_id=product.id).first()
    print(f"wishlist_item: {wishlist_item}")
    if not wishlist_item:
        new_wishlist_item = Wishlist(user_id=1, product_id=product.id)
        db.session.add(new_wishlist_item)
        db.session.commit()
        flash(f'Added {product.name} to wishlist.')
    else:
        flash('Item already in wishlist.')

    return redirect(url_for('index'))


@flask_app.route('/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist():
    product_id = request.form.get('product_id')
    wishlist_item = Wishlist.query.filter_by(product_id=product_id).first()

    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Item removed from wishlist.')
    else:
        flash('Item not found in wishlist.')

    return redirect(url_for('wishlist'))


@flask_app.route('/checkout', methods=['POST'])
def checkout():
    Cart.query.delete()
    db.session.commit()
    flash('Checkout complete!')
    return redirect(url_for('index'))


db.init_app(flask_app)


with flask_app.app_context():
    db.create_all()


@flask_app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    product_name = form_data.get('product_name')
    price = form_data.get('price')
    desc = form_data.get('description')
    category = form_data.get('category')
    stock = form_data.get('size')
    product = Product(
        name=product_name,
        price=price,
        desc=desc,
        category=category,
        stock=stock)
    db.session.add(product)
    db.session.commit()
    print("sumitted successfully")
    return redirect('/add-product')


if __name__ == '__main__':
    flask_app.run(
        host='127.0.0.1',
        port=8005,
        debug=True
    )