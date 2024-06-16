from flask import Flask
from dotenv import load_dotenv
import secrets

secret_key = secrets.token_hex(16)


def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app