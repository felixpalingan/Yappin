from flask_socketio import emit, join_room, leave_room
from extensions import socketio, db
from models import Message, User

# Event saat user connect ke socket
@socketio.on('connect')
def handle_connect():
    print("Client connected!")

# Event saat user join room chat tertentu
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(f"{username} masuk ke room {room}")
    # Opsional: Kasih tau user lain di room itu
    emit('status', {'msg': username + ' has entered the room.'}, room=room)

# Event saat user kirim pesan
@socketio.on('send_message')
def on_send_message(data):
    username = data['username']
    room = data['room']
    content = data['message']

    print(f"Pesan dari {username} di {room}: {content}")

    # 1. Simpan ke Database
    user = User.query.filter_by(username=username).first()
    if user:
        new_msg = Message(content=content, sender_id=user.id, room=room)
        db.session.add(new_msg)
        db.session.commit()

        # 2. Broadcast pesan ke SEMUA orang di room itu (termasuk pengirim)
        # Kita balikin data lengkap termasuk timestamp dari server
        emit('new_message', new_msg.to_json(), room=room)
    else:
        print("User gak ditemukan, pesan gagal disimpan")