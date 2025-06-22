from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from app import db
from app.models import Product, User
from app.catalog.orders_models import Order
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

UPLOAD_FOLDER = 'static/img/products'

def is_admin():
    user_id = session.get("user_id")
    if not user_id:
        return False
    user = User.query.get(user_id)
    return user and user.is_admin

# Панель адміністратора
@admin_bp.route('/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('auth.login'))

    stats = {
        "orders": Order.query.count(),
        "products": Product.query.count(),
        "users": User.query.count(),
        "revenue": sum([eval(o.items).get("total_price", 0) for o in Order.query.all()])
    }

    return render_template('admin/dashboard.html', stats=stats)

# Всі товари (по категоріях)
@admin_bp.route('/products')
def admin_products():
    if not is_admin():
        return redirect(url_for('auth.login'))

    products = Product.query.all()
    categories = {
        "Собаки": [],
        "Коти": [],
        "Гризуни": [],
        "Риби": [],
        "Птахи": [],
        "Рептилії": [],
        "Інше": []
    }

    for product in products:
        if hasattr(product, 'category') and product.category in categories:
            categories[product.category].append(product)
        else:
            categories["Інше"].append(product)

    return render_template('admin/products.html', categories=categories)

# Усі товари в таблиці
@admin_bp.route('/products/table')
def products_table():
    if not is_admin():
        return redirect(url_for('auth.login'))

    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/products_table.html', products=products)

from flask import request, redirect, url_for, flash, render_template
from app.models import Product, ProductWeight
from app import db
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/img/products'

# Додавання товару
@admin_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if not is_admin():
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])  # базова ціна (можеш залишити, або зробити необов'язковою)
        old_price = float(request.form.get('old_price') or 0)
        brand = request.form['brand']
        category = request.form['category']
        discount = int(request.form.get('discount') or 0)
        details = request.form['details']
        characteristics = request.form['characteristics']
        show_on_main = bool(request.form.get('show_on_main'))
        main_category = request.form['main_category']
        sub_category = request.form.get('sub_category') or ''


        # Основне зображення
        image_file = request.files['image']
        image_filename = None
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(UPLOAD_FOLDER, image_filename))

        # Галерея
        gallery_filenames = []
        gallery_files = request.files.getlist('gallery')
        for file in gallery_files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                gallery_filenames.append(filename)

        # Створення об'єкта продукту
        new_product = Product(
            name=name,
            description=description,
            price=price,  # залиш для загальної сумісності
            old_price=old_price,
            brand=brand,
            weight=None,  # замінюємо вагу на окремі фасування
            category=category,
            discount=discount,
            image=f"img/products/{image_filename}" if image_filename else None,
            gallery=';'.join([f"img/products/{f}" for f in gallery_filenames]),
            details=details,
            characteristics=characteristics,
            show_on_main=show_on_main,
            main_category=main_category,
            sub_category=sub_category
        )

        db.session.add(new_product)
        db.session.commit()  # Щоб отримати ID продукту

        # ⬇️ ЗБЕРІГАННЯ ВСІХ ФАСУВАНЬ
        weights = request.form.to_dict(flat=False)
        index = 0

        while True:
            try:
                amount = weights[f'weights[{index}][amount]'][0]
                unit = weights[f'weights[{index}][unit]'][0]
                weight_price = float(weights[f'weights[{index}][price]'][0])

                new_weight = ProductWeight(
                    product_id=new_product.id,
                    amount=amount,
                    unit=unit,
                    price=weight_price
                )
                db.session.add(new_weight)
                index += 1
            except KeyError:
                break  # Закінчились усі ваги

        db.session.commit()

        flash("✅ Товар успішно додано з усіма фасуваннями!", "success")
        return redirect(url_for('admin.add_product'))

    return render_template('admin/add_product.html')


# Редагування товару
@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not is_admin():
        return redirect(url_for('auth.login'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.show_on_main = bool(request.form.get('show_on_main'))
        product.main_category = request.form.get('main_category')
        product.sub_category = request.form.get('sub_category')
        db.session.commit()
        flash("📝 Товар оновлено!", "info")
        return redirect(url_for('admin.admin_products'))

    return render_template('admin/edit_product.html', product=product)

# Замовлення
@admin_bp.route('/orders')
def admin_orders():
    if not is_admin():
        return redirect(url_for('auth.login'))

    orders = Order.query.order_by(Order.timestamp.desc()).all()
    return render_template('admin/orders.html', orders=orders)

# Користувачі
@admin_bp.route('/users')
def admin_users():
    if not is_admin():
        return redirect(url_for('auth.login'))

    users = User.query.all()
    return render_template('admin/users.html', users=users)

# Налаштування
@admin_bp.route('/settings')
def admin_settings():
    if not is_admin():
        return redirect(url_for('auth.login'))

    return render_template('admin/settings.html')



@admin_bp.route('/products/<int:product_id>/toggle-main', methods=['POST'])
def toggle_show_on_main(product_id):
    if not is_admin():
        return redirect(url_for('auth.login'))

    product = Product.query.get_or_404(product_id)
    product.show_on_main = not product.show_on_main
    db.session.commit()
    flash("✅ Статус оновлено!", "success")
    return redirect(url_for('admin.products_table'))

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if not is_admin():
        return redirect(url_for('auth.login'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("🗑️ Товар видалено!", "success")
    return redirect(url_for('admin.products_table'))
