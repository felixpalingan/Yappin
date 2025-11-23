import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import db, jwt, socketio, cors
from routes.auth import auth_bp
from routes.chat import chat_bp # Import route chat
import events # Import events biar SocketIO jalan

load_dotenv()

def create_app():
    app = Flask(__name__)

    database_url = os.getenv('DATABASE_URL')

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or "sqlite:///yappin.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    socketio.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat') # Register chat route

    # Create Database Tables (User & Message)
    with app.app_context():
        db.create_all()

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Server Yappin jalan bro!", "status": "online"})

    return app

if __name__ == '__main__':
    app = create_app()
    # Host 0.0.0.0 wajib biar bisa diakses dari HP (di jaringan WiFi yg sama)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)