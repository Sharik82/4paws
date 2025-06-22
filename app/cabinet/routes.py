from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app import db
from app.models import User, Favorite, Product

cabinet_bp = Blueprint('cabinet', __name__, template_folder='templates/cabinet')

# Профіль
@cabinet_bp.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    return render_template("cabinet/profile.html", user=user)

# Замовлення
@cabinet_bp.route('/orders')
def orders():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    return render_template("cabinet/orders.html", user=user)

# Методи оплати
@cabinet_bp.route('/payments')
def payments():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    return render_template("cabinet/payments.html", user=user)

# Налаштування
@cabinet_bp.route('/settings')
def settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    return render_template("cabinet/settings.html", user=user)

# Обране - додати/видалити
@cabinet_bp.route("/favorite", methods=["POST"])
def toggle_favorite():
    if "user_id" not in session:
        return jsonify({"error": "not_logged_in"}), 401

    data = request.get_json()
    product_id = data.get("id")
    user_id = session["user_id"]

    fav = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"status": "removed"})
    else:
        new_fav = Favorite(user_id=user_id, product_id=product_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"status": "added"})

# Перегляд обраного
@cabinet_bp.route('/favorites')
def favorites():
    if "user_id" not in session:
        return redirect(url_for('auth.login'))

    favorites = Favorite.query.filter_by(user_id=session["user_id"]).all()
    product_ids = [f.product_id for f in favorites]
    products = Product.query.filter(Product.id.in_(product_ids)).all()

    return render_template("cabinet/favorites.html", products=products)
