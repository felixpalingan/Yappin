from flask import Blueprint, request, jsonify
from extensions import db
from models import Message
from flask_jwt_extended import jwt_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/history/<room_name>', methods=['GET'])
@jwt_required() # Harus login dulu
def get_chat_history(room_name):
    # Ambil semua pesan di room itu, urutkan dari yang terlama ke terbaru
    messages = Message.query.filter_by(room=room_name).order_by(Message.timestamp.asc()).all()
    
    output = []
    for msg in messages:
        output.append(msg.to_json())

    return jsonify(output), 200