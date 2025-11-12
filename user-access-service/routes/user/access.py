from json import dumps

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from repository.iot_data import truncate_mongo_data, get_data, get_device_owner_id
from repository.user_data import get_user_device_ids, truncate_user_data


user_access_bp = Blueprint('user_access', __name__)

@user_access_bp.route('/retrieve', methods=['GET'])
@jwt_required()
def user_retrieve():
    user_id = get_jwt_identity().get('user_id')
    device_id = request.get_json().get('device_id')

    if not device_id:
        return {
            "message": "Device ID is required"
        }, 400

    if user_id != get_device_owner_id(device_id):
        return {
            "message": "Unauthorized access to device data"
        }, 403

    page = request.get_json().get('page', 1)
    size = request.get_json().get('size', 10)

    device_data = get_data(device_id, page, size)

    return {"data": device_data}, 200


@user_access_bp.route('/devices', methods=['GET'])
@jwt_required()
def user_devices():
    user_id = get_jwt_identity().get('user_id')
    device_ids = get_user_device_ids(user_id)

    device_ids = device_ids if device_ids else []

    return {"device_ids": device_ids}, 200


@user_access_bp.route('/truncate', methods=['DELETE'])
def user_truncate():
    truncate_user_data()
    truncate_mongo_data()
    return {"message": "User Truncate Endpoint"}, 200
