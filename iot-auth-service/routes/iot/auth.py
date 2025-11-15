from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from repository.iot_data import create_device_in_db, get_device_from_db


iot_auth_bp = Blueprint('iot_auth', __name__)


@iot_auth_bp.route('/login', methods=['GET'])
def iot_login():
    body = request.get_json()
    device_mac: str = body.get('mac', None)

    device = get_device_from_db(device_mac)

    if device:
        access_token = create_access_token(identity={"device_id": device['id'], "role": "device"})
        refresh_token = create_refresh_token(identity={"device_id": device['id'], "role": "device"})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200

    return {
        "message": "Invalid device credentials"
    }, 401


@iot_auth_bp.route('/register', methods=['POST'])
def iot_register():
    body = request.get_json()
    device_mac: str = body.get('mac', None)
    device_type: str = body.get('type', None)

    device = get_device_from_db(device_mac)
    if device:
        return {
            "message": "Device already registered"
        }, 409

    device_id = create_device_in_db(device_mac, device_type)

    if device_id:
        access_token = create_access_token(identity={"device_id": device_id, "role": "device"})
        refresh_token = create_refresh_token(identity={"device_id": device_id, "role": "device"})

        return {
            "message": "Device registered successfully",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 201

    return {
        "message": "Device registration failed"
    }, 500


@iot_auth_bp.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def iot_refresh():
    current_device = get_jwt_identity()
    if current_device['role'] != 'device':
        return {
            "message": "Invalid token role"
        }, 401

    new_access_token = create_access_token(identity=current_device)

    return {
        "access_token": new_access_token
    }, 200
