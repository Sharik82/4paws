
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv
from datetime import timedelta


db = SQLAlchemy()

def create_app():
    
    load_dotenv()

    
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    
    app.permanent_session_lifetime = timedelta(days=30)  # Конфіг на місяць

    
    app.secret_key = os.getenv("SECRET_KEY")

    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath('instance/users.db')}"

    
    app.config["SQLALCHEMY_BINDS"] = {
        'products': f"sqlite:///{os.path.abspath('instance/products.db')}"
    }

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)  

    #  Ініціалізація
    Session(app)
    db.init_app(app)

    #  Blueprints
    from app.auth.routes import auth_bp
    from app.catalog.routes import catalog_bp
    from app.admin.routes import admin_bp
    from app.cabinet.routes import cabinet_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cabinet_bp, url_prefix='/cabinet')

    return app
