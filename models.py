from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Relasi biar gampang akses message dari user
    messages = db.relationship('Message', backref='sender', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Siapa yang ngirim
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Nama Room. 
    # Logic: Kalau chat personal user A & B, nama roomnya: "userA_userB" (disortir abjad biar konsisten)
    room = db.Column(db.String(50), nullable=False) 

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "sender": self.sender.username,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }