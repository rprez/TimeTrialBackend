from flask import current_app, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.users import users_blueprint

@users_blueprint.route('/<user_id>', methods=['GET'])
@jwt_required()
def view_user(user_id):
    auth_user_id = get_jwt_identity()

    current_app.logger.info('{} viewing profile of {} (GET)'.format(auth_user_id, user_id))
    user_raw = { "user": { "number_players":4, "play_time": '10:30', "sio_uid":'player0003', "sio_to":'admin', "auth_code":'1234', "reserve_time":'1211233049545' } }

    if not user_raw:
        return jsonify({'Error': 'User not found.'}), 404

    return jsonify(user_raw), 200