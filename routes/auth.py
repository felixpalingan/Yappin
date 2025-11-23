from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username dan password wajib diisi bro"}), 400

    # Cek username udah ada belum
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username udah dipake orang lain"}), 400

    # Bikin user baru
    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Registrasi berhasil!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    # Cek user ada gak & password bener gak
    if not user or not user.check_password(password):
        return jsonify({"msg": "Username atau password salah"}), 401

    # Bikin JWT Token (Identity pake ID user biar unik)
    access_token = create_access_token(identity=str(user.id)) # Convert ke string biar aman

    return jsonify({
        "msg": "Login sukses",
        "access_token": access_token,
        "username": user.username,
        "user_id": user.id
    }), 200