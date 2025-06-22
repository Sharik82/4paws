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
class Favorite(db.Model):  # зберігається в users.db
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

#Товар
class Product(db.Model):
    __bind_key__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float, nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    discount = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    gallery = db.Column(db.Text, nullable=True)
    details = db.Column(db.Text, nullable=True)
    characteristics = db.Column(db.Text, nullable=True)
    main_category = db.Column(db.String(100), nullable=True)
    sub_category = db.Column(db.String(100), nullable=True)
    show_on_main = db.Column(db.Boolean, default=False)

    #Звʼязок з таблицею фасувань
    weights = db.relationship('ProductWeight', backref='product', lazy=True)

    # Для API 
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
            "discount": self.discount,
            "image": self.image,
            "gallery": self.gallery,
            "details": self.details,
            "characteristics": self.characteristics,
            "main_category": self.main_category,
            "sub_category": self.sub_category,
            "show_on_main": self.show_on_main
        }

    #JSON-формат фасувань для шаблону
    @property
    def weights_json(self):
        return [
            {
                "weight": w.amount,
                "unit": w.unit,
                "price": w.price
            } for w in self.weights
        ]

#Фасування (вага + ціна)
class ProductWeight(db.Model):
    __bind_key__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    amount = db.Column(db.String(20))  
    unit = db.Column(db.String(20))    
    price = db.Column(db.Float)
