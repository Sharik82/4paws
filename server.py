import os
from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv  # Додаємо dotenv для роботи з .env

# 🔹 Завантажуємо змінні середовища
load_dotenv()

app = Flask(__name__, template_folder="templates")

# 🔹 Використовуємо SECRET_KEY
app.secret_key = os.getenv("SECRET_KEY")

# 🔹 Гарантуємо правильний шлях до бази даних
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Отримуємо шлях до кореня проєкту
DATABASE_PATH = os.path.join(BASE_DIR, "instance", "users.db")  # Формуємо правильний шлях

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🔹 Налаштування сесій
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

db = SQLAlchemy(app)


# 📌 **Модель користувача**
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

# 📌 **Модель товару**
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # URL до зображення товару

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url
        }

# 📌 **Головна сторінка**
@app.route('/')
def index():
    products = Product.query.all()  # Отримуємо всі товари з БД
    return render_template('index.html', products=products)

# 📌 **Категорії товарів**
@app.route('/categories/dogs')
def dog_category():
    return render_template('categories/dog.html')

@app.route('/categories/cats')
def cat_category():
    return render_template('categories/cat.html')

@app.route('/categories/rodents')
def rodents_category():
    return render_template('categories/rodents.html')

@app.route('/categories/fish')
def fish_category():
    return render_template('categories/fish.html')

@app.route('/categories/dove')
def dove_category():
    return render_template('categories/dove.html')

@app.route('/categories/snake')
def snake_category():
    return render_template('categories/snake.html')

# 📌 **Маршрут для отримання всіх товарів у JSON**
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

# 📌 **Сторінка товару**
@app.route("/product/<int:product_id>")
def product_page(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Товар не знайдено", 404
    return render_template("product.html", product=product)

# 📌 **Пошук товарів (API)**
@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify([])  # Повертаємо пустий список, якщо запит порожній

    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    return jsonify([product.to_dict() for product in products])

# 📌 **Сторінка оформлення замовлення**
@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])

    # Перетворюємо товари з ID на об'єкти з бази
    detailed_cart = [Product.query.get(item).to_dict() for item in cart if Product.query.get(item)]
    
    return render_template('checkout.html', cart=detailed_cart)

# 📌 **API для роботи з кошиком**
@app.route("/api/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = []  # Ініціалізуємо кошик, якщо його немає

    if request.method == "POST":
        data = request.json
        product = Product.query.get(data.get("id"))  # Перевіряємо, чи товар є в БД
        if product:
            session["cart"].append(product.id)  # Додаємо товар у кошик за ID
            session.modified = True
            return jsonify({"message": "Товар додано в кошик", "cart": session["cart"]})
        return jsonify({"error": "Товар не знайдено"}), 404

    return jsonify(session["cart"])  # Повертаємо вміст кошика

# 📌 **API для очищення кошика**
@app.route("/api/cart/clear", methods=["POST"])
def clear_cart():
    session["cart"] = []
    session.modified = True
    return jsonify({"message": "Кошик очищено"})

# 📌 **Запуск сервера**
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5050, debug=True)
