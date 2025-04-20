from flask_socketio import emit, join_room, leave_room
from flask import request
from src.startup import socketio
from src.utils.logger import logger
from datetime import datetime
from collections import defaultdict
import time


user_rate_limit = defaultdict(lambda: 0)


active_rooms = defaultdict(lambda: {'users': set(), 'authorized_roles': ['admin', 'driver']})


MAX_RATE_LIMIT_SECONDS = 5


def is_user_authorized_for_room(user_role, room):
    
    return user_role in active_rooms[room]['authorized_roles']


@socketio.on('connect')
def handle_connect():
    logger.info(f"[SocketIO] Client connected: {request.sid}")
    emit('connection_ack', {'msg': 'Connection established successfully.'})


@socketio.on('disconnect')
def handle_disconnect():
    
    for room in list(active_rooms):
        if request.sid in active_rooms[room]['users']:
            active_rooms[room]['users'].remove(request.sid)
            logger.info(f"[SocketIO] Client {request.sid} disconnected from room {room}")
    
    logger.info(f"[SocketIO] Client disconnected: {request.sid}")


@socketio.on('join')
def handle_join(data):
    try:
        room = data.get('room')
        user_role = data.get('role')  
        if not room or not user_role:
            emit('error', {'msg': 'Room and user role are required.'})
            logger.warning(f"[SocketIO] Join failed: no room or role provided by {request.sid}")
            return

        if room not in active_rooms:
            active_rooms[room] = {'users': set(), 'authorized_roles': ['admin', 'driver']}  # Create room

        if not is_user_authorized_for_room(user_role, room):
            emit('error', {'msg': f'You are not authorized to join the room {room}.'})
            logger.warning(f"[SocketIO] Join failed: unauthorized user role {user_role} for room {room} by {request.sid}")
            return

        join_room(room)
        active_rooms[room]['users'].add(request.sid)
        logger.info(f"[SocketIO] Client {request.sid} joined room {room}")
        emit('status', {'msg': f'{request.sid} joined room: {room}'}, room=room)

    except Exception as e:
        logger.error(f"[SocketIO] Error on join: {str(e)}", exc_info=True)
        emit('error', {'msg': 'Failed to join room'})


@socketio.on('location_update')
def handle_location_update(data):
    try:
        room = data.get('room')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        user_role = data.get('role')  

        
        if not all([room, latitude, longitude, user_role]):
            emit('error', {'msg': 'Room, latitude, longitude, and user role are required'})
            logger.warning(f"[SocketIO] Incomplete location data from {request.sid}: {data}")
            return

       
        if room not in active_rooms:
            emit('error', {'msg': f'Room {room} does not exist.'})
            logger.warning(f"[SocketIO] Invalid room {room} from {request.sid}")
            return

        if not is_user_authorized_for_room(user_role, room):
            emit('error', {'msg': f'You are not authorized to update location in room {room}.'})
            logger.warning(f"[SocketIO] Unauthorized location update attempt by {request.sid} in room {room}")
            return

       
        current_time = time.time()
        if current_time - user_rate_limit[request.sid] < MAX_RATE_LIMIT_SECONDS:
            emit('error', {'msg': 'Rate limit exceeded. Try again later.'})
            logger.warning(f"[SocketIO] Rate limit exceeded for {request.sid} in room {room}")
            return

        
        user_rate_limit[request.sid] = current_time

       
        logger.info(f"[SocketIO] Location update from {request.sid} to room {room} — lat: {latitude}, lon: {longitude}")
        emit('update_driver_location', {
            'sid': request.sid,
            'latitude': latitude,
            'longitude': longitude
        }, room=room)

    except Exception as e:
        logger.error(f"[SocketIO] Error in location_update: {str(e)}", exc_info=True)
        emit('error', {'msg': 'Failed to update location'})
