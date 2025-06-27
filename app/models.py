from app import db

#Користувач
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    lastname = db.Column(db.String(100))
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

#Обране
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

# Категорія товарів
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    parent = db.relationship('Category', remote_side=[id], backref='children')

    def __repr__(self):
        return f'<Category {self.name}>'

#Товар
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float, nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category_rel = db.relationship('Category', backref='products')
    discount = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    gallery = db.Column(db.Text, nullable=True)
    details = db.Column(db.Text, nullable=True)
    characteristics = db.Column(db.Text, nullable=True)
    main_category = db.Column(db.String(100), nullable=True)
    sub_category = db.Column(db.String(100), nullable=True)
    show_on_main = db.Column(db.Boolean, default=False)

    #Звʼязок з фасуваннями
    weights = db.relationship('ProductWeight', backref='product', lazy=True)

    #Словник для API
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "old_price": self.old_price,
            "brand": self.brand,
            "weight": self.weight,
            "category": self.category,
            "category_id": self.category_id,
            "discount": self.discount,
            "image": self.image,
            "gallery": self.gallery,
            "details": self.details,
            "characteristics": self.characteristics,
            "main_category": self.main_category,
            "sub_category": self.sub_category,
            "show_on_main": self.show_on_main
        }

    #JSON для шаблону
    @property
    def weights_json(self):
        return [
            {
                "weight": w.amount,
                "unit": w.unit,
                "price": w.price
            } for w in self.weights
        ]

#Фасування
class ProductWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    amount = db.Column(db.String(20))  
    unit = db.Column(db.String(20))    
    price = db.Column(db.Float)
