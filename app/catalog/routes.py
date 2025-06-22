from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from app.models import Product
from app.catalog.orders_models import Order
from app import db
import json

catalog_bp = Blueprint('catalog', __name__)

#Головна сторінка
@catalog_bp.route('/')
@catalog_bp.route('/index', endpoint='index')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Обробка товарів з JS → session['cart']
@catalog_bp.route('/go-to-orders', methods=['POST'])
def go_to_orders():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Порожній кошик'}), 400

    session_cart = []

    for item in data:
        clean_name = item['name'].split(' (')[0].strip()  # видаляє (5 кг)
        quantity = int(item.get('quantity', 1))
        price = float(item.get('price', 0))
        weight = item.get('name').split('(')[-1].replace(')', '') if '(' in item['name'] else ''

        product = Product.query.filter_by(name=clean_name).first()
        if product:
            session_cart.append({
                "id": product.id,
                "quantity": quantity,
                "price": price,
                "weight": weight,
                "image": product.image,
                "name": product.name,
                "total": round(quantity * price, 2),
                "description": product.description or ''
            })

    session["cart"] = session_cart
    session.modified = True
    return jsonify({'redirect': url_for('catalog.orders')})


# Сторінка оформлення замовлення
@catalog_bp.route('/orders', methods=['GET', 'POST'])
def orders():
    cart = session.get('cart', [])
    detailed_cart = []
    total_price = 0

    for entry in cart:
        product = Product.query.get(entry["id"])
        if product:
            item_data = product.to_dict()
            item_data["quantity"] = entry.get("quantity", 1)
            item_data["price"] = entry.get("price", product.price)
            item_data["weight"] = entry.get("weight", '')
            item_data["total"] = round(item_data["price"] * item_data["quantity"], 2)
            total_price += item_data["total"]
            detailed_cart.append(item_data)

    if request.method == 'POST':
        full_name = request.form.get("fullName")
        phone = request.form.get("phone")
        delivery_method = request.form.get("deliveryMethod")
        city = request.form.get("city")
        branch = request.form.get("branch")
        payment_method = request.form.get("paymentMethod")

        order_info = {
            "customer": {
                "fullName": full_name,
                "phone": phone,
                "deliveryMethod": delivery_method,
                "city": city,
                "branch": branch,
                "paymentMethod": payment_method
            },
            "items": detailed_cart
        }

        new_order = Order(items=json.dumps(order_info, ensure_ascii=False))
        db.session.add(new_order)
        db.session.commit()

        session["cart"] = []
        flash("Ваше замовлення успішно оформлене!")
        return redirect(url_for('catalog.index'))

    return render_template('orders.html', cart=detailed_cart, total_price=total_price)


#Каталоги та категорії
@catalog_bp.route('/catalog/Lasoshchi')
def lasoshchi():
    return render_template('catalog/Lasoshchi.html')

@catalog_bp.route('/categories/dogs')
def dog_category():
    return render_template('categories/dog.html')

@catalog_bp.route('/categories/cats')
def cat_category():
    return render_template('categories/cat.html')

@catalog_bp.route('/categories/rodents')
def rodents_category():
    return render_template('categories/rodents.html')

@catalog_bp.route('/categories/fish')
def fish_category():
    return render_template('categories/fish.html')

@catalog_bp.route('/categories/dove')
def dove_category():
    return render_template('categories/dove.html')

@catalog_bp.route('/categories/snake')
def snake_category():
    return render_template('categories/snake.html')

# Сторінки окремих товарів

@catalog_bp.route("/product/PR2")
def pr2_page():
    return render_template("products/PR2.html")

@catalog_bp.route("/product/PR3")
def pr3_page():
    return render_template("products/PR3.html")

@catalog_bp.route("/product/PR4")
def pr4_page():
    return render_template("products/PR4.html")

@catalog_bp.route("/product/PR5")
def pr5_page():
    return render_template("products/PR5.html")

@catalog_bp.route("/product/PR6")
def pr6_page():
    return render_template("products/PR6.html")

#API: товари, пошук, кошик
@catalog_bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])



@catalog_bp.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    detailed_cart = [Product.query.get(item["id"]).to_dict() for item in cart if Product.query.get(item["id"])]
    return render_template('checkout.html', cart=detailed_cart)

@catalog_bp.route("/api/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":
        data = request.json
        product = Product.query.get(data.get("id"))
        if product:
            session["cart"].append({"id": product.id, "quantity": data.get("quantity", 1)})
            session.modified = True
            return jsonify({"message": "Товар додано в кошик", "cart": session["cart"]})
        return jsonify({"error": "Товар не знайдено"}), 404

    return jsonify(session["cart"])

@catalog_bp.route("/api/cart/clear", methods=["POST"])
def clear_cart():
    session["cart"] = []
    session.modified = True
    return jsonify({"message": "Кошик очищено"})


@catalog_bp.route('/catalog/dogs/dogcatalog', endpoint='dogcatalog')
def dog_food():
    products = Product.query.filter_by(sub_category='dogcatalog').all()
    return render_template('catalog/dogs/dogcatalog.html', products=products)

from flask import render_template
from app.models import Product  

@catalog_bp.route('/product/<int:product_id>')
def product_page(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/product.html', product=product)

from flask import render_template
from app.models import Product

#Собаки — підкатегорії
@catalog_bp.route('/catalog/dogs/treats')
def dog_treats():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_treats").all()
    return render_template('catalog/dogs/dog_treats.html', products=products)

@catalog_bp.route('/catalog/dogs/toys')
def dog_toys():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_toys").all()
    return render_template('catalog/dogs/dog_toys.html', products=products)

@catalog_bp.route('/catalog/dogs/sets')
def dog_sets():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_sets").all()
    return render_template('catalog/dogs/dog_sets.html', products=products)

@catalog_bp.route('/catalog/dogs/gear')
def dog_gear():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_gear").all()
    return render_template('catalog/dogs/dog_gear.html', products=products)

@catalog_bp.route('/catalog/dogs/supplements')
def dog_supplements():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_supplements").all()
    return render_template('catalog/dogs/dog_supplements.html', products=products)

@catalog_bp.route('/catalog/dogs/meds')
def dog_meds():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_meds").all()
    return render_template('catalog/dogs/dog_meds.html', products=products)

@catalog_bp.route('/catalog/dogs/carriers')
def dog_carriers():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_carriers").all()
    return render_template('catalog/dogs/dog_carriers.html', products=products)

@catalog_bp.route('/catalog/dogs/beds')
def dog_beds():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_beds").all()
    return render_template('catalog/dogs/dog_beds.html', products=products)

@catalog_bp.route('/catalog/dogs/clothes')
def dog_clothes():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_clothes").all()
    return render_template('catalog/dogs/dog_clothes.html', products=products)

@catalog_bp.route('/catalog/dogs/accessories')
def dog_accessories():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_accessories").all()
    return render_template('catalog/dogs/dog_accessories.html', products=products)

@catalog_bp.route('/catalog/dogs/bowls')
def dog_bowls():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_bowls").all()
    return render_template('catalog/dogs/dog_bowls.html', products=products)

@catalog_bp.route('/catalog/dogs/care')
def dog_care():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_care").all()
    return render_template('catalog/dogs/dog_care.html', products=products)

@catalog_bp.route('/catalog/dogs/toilets')
def dog_toilets():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_toilets").all()
    return render_template('catalog/dogs/dog_toilets.html', products=products)

@catalog_bp.route('/catalog/dogs/cleaners')
def dog_cleaners():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_cleaners").all()
    return render_template('catalog/dogs/dog_cleaners.html', products=products)

@catalog_bp.route('/catalog/dogs/smart')
def dog_smart():
    products = Product.query.filter_by(main_category="Собаки", sub_category="dog_smart").all()
    return render_template('catalog/dogs/dog_smart.html', products=products)

from flask import request, jsonify, url_for
from app.models import Product
from app import db
from sqlalchemy import or_

@catalog_bp.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()

    if not query:
        return jsonify([])

    terms = query.split()

    products = Product.query.filter(
        or_(
            *[Product.name.ilike(f"%{term}%") for term in terms],
            *[Product.description.ilike(f"%{term}%") for term in terms]
        )
    ).all()

    return jsonify([
        {
            "name": product.name,
            "price": f"{product.price:.2f}",
            "image": url_for('static', filename=product.image),
            "url": url_for('catalog.product_page', product_id=product.id)
        }
        for product in products
    ])
