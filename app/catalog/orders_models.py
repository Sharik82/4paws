from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Text, nullable=False)  # JSON 
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
