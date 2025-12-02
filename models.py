from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import secrets
import string

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    certificates = db.relationship('Certificate', backref='owner', lazy=True, cascade='all, delete-orphan')
    access_codes = db.relationship('AccessCode', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f"user_{self.id}"

class Company(UserMixin, db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f"company_{self.id}"

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_hash = db.Column(db.String(64), nullable=False, unique=True)  # SHA-256 hash
    file_type = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    blockchain_block_id = db.Column(db.Integer, nullable=True)  # Reference to blockchain block
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class AccessCode(db.Model):
    __tablename__ = 'access_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), unique=True, nullable=False)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificates.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    certificate = db.relationship('Certificate', backref='access_codes', lazy=True)
    
    @staticmethod
    def generate_code():
        """Generate a secure 12-character access code"""
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(12))
    
    def is_valid(self):
        """Check if access code is valid and not expired"""
        return self.is_active and datetime.utcnow() < self.expires_at

class BlockchainBlock(db.Model):
    __tablename__ = 'blockchain_blocks'
    
    id = db.Column(db.Integer, primary_key=True)
    block_hash = db.Column(db.String(64), nullable=False, unique=True)
    previous_hash = db.Column(db.String(64), nullable=False)
    certificate_hash = db.Column(db.String(64), nullable=False)  # The certificate hash stored in this block
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    nonce = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Block {self.id}: {self.block_hash[:10]}...>'
