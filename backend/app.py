import os
from flask import Flask , jsonify
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()  # Load .env file

from config import Config
from extensions import db, migrate, jwt
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from models.users import User
    from models.cars import Cars
    from models.booking import Booking
    from models.payments import Payment

    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp,url_prefix = "/api/auth")


    return app

app = create_app()

# list = [{"name":"anas","class":"middle"},
#         {"name":"anas","class":"middle"}]
# @app.route("/")
# def index():
#     return jsonify(list)
if __name__ == "__main__":
    app.run(debug=True)