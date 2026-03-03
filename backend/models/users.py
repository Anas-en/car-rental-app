from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False , default="renter")  # owner or renter
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    cars = db.relationship("Cars", backref="owner", lazy=True, cascade="all, delete")

    def set_password(self , password):
        self.password_hash = generate_password_hash(password)

    def check_password (self,password):
        return check_password_hash(self.password_hash , password)
    