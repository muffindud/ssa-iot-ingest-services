from flask import Blueprint, Flask, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import bcrypt

from repository.user_data import get_user_from_db, create_user_in_db, get_user_id, link_device_to_user
from repository.iot_data import get_device_from_db, get_device_owner_id


user_auth_bp = Blueprint('user_auth', __name__)


@user_auth_bp.route('/login', methods=['GET'])
def user_login():
    body = request.get_json()
    username: str = body.get('username', None)
    password: str = body.get('password', None)

    user = get_user_from_db(username)

    if not user:
        return {
            "message": "Invalid credentials"
        }, 401

    if isinstance(user['password_hash'], memoryview):
        stored_bytes = user['password_hash'].tobytes()
    elif isinstance(user['password_hash'], bytes):
        stored_bytes = user['password_hash']
    elif isinstance(user['password_hash'], str) and user['password_hash'].startswith("\\x"):
        stored_bytes = bytes.fromhex(user['password_hash'][2:])

    if user and bcrypt.checkpw(password.encode('utf-8'), stored_bytes):
        access_token = create_access_token(identity={"user_id": user['id'], "role": "user"})
        refresh_token = create_refresh_token(identity={"user_id": user['id'], "role": "user"})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200

    return {
        "message": "Invalid credentials"
    }, 401


@user_auth_bp.route('/register', methods=['POST'])
def user_register():
    body = request.get_json()
    username: str = body.get('username', None)
    password: str = body.get('password', None)

    if get_user_id(username) is not None:
        return {
            "message": "Username already exists"
        }, 409

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_id = create_user_in_db(username, password_hash)

    if user_id:
        access_token = create_access_token(identity={"user_id": user_id, "role": "user"})
        refresh_token = create_refresh_token(identity={"user_id": user_id, "role": "user"})

        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 201

    return {
        "message": "User registration failed"
    }, 500


@user_auth_bp.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def user_refresh():
    current_user = get_jwt_identity()
    if current_user['role'] != 'user':
        return {
            "message": "Invalid token role"
        }, 401

    new_access_token = create_access_token(identity=current_user)

    return {
        "access_token": new_access_token
    }, 200


@user_auth_bp.route('/link', methods=['POST'])
@jwt_required()
def user_link_device():
    identity = get_jwt_identity()
    if identity['role'] != 'user':
        return {
            "message": "Unauthorized"
        }, 403

    user_id = identity['user_id']
    body = request.get_json()
    device_mac: str = body.get('mac', None)

    device = get_device_from_db(device_mac)
    if not device:
        return {
            "message": "Device not found"
        }, 404

    device_id = device['id']

    owner_id = get_device_owner_id(device_id)
    if owner_id is not None:
        return {
            "message": "Device already linked to a user"
        }, 409

    link_id = link_device_to_user(user_id, device_id)

    if link_id:
        return {
            "message": "Device linked successfully"
        }, 200

    return {
        "message": "Failed to link device"
    }, 500
