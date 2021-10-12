from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt_identity,get_jwt

from app.auth import auth_blueprint


@auth_blueprint.route('/login', methods=['POST'])
def login():
    json_input = request.get_json(force=True)

    try:
        auth_code = json_input['auth_code']
    except KeyError as e:
        return jsonify({'Error': 'Invalid request: Missing required field.'}), 400
    except TypeError as e:
        return jsonify({'Error': 'Invalid request: Must be a json/dict.'}), 400

    if len(auth_code) == 0 or auth_code == '':
        return jsonify({'Error': 'Please provide a auth_code.'}), 400

    if request.method == 'POST':
        try:
            #Find in DataBase
            if auth_code == "12345":
                user = {"game":"12345","team":"Blue"}
            else:
                return jsonify({'Error': 'User not found.'}), 400

            if not user:
                return jsonify({'Error': 'User not found.'}), 400

        except TypeError as e:
            return jsonify({'Error': 'Bad auth_code.'}), 400

        if user:
            access_token = create_access_token(identity=auth_code, fresh=True)
            refresh_token = create_refresh_token(identity=auth_code)

            current_app.logger.info('Login')

            return jsonify({'session_token': access_token, 'refresh_token': refresh_token}), 200

        else:
            current_app.logger.info('%s failed to log in', auth_code)  # wrong auth_code
            return jsonify({'Error': 'Invalid auth_code.'}), 403
    else:
        return jsonify({'Error': 'Request must be POST'}), 405


@auth_blueprint.route("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id, fresh=True)

    return jsonify({'Token': access_token})


@auth_blueprint.route('/logout', methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()['jti']

    return jsonify({'Success': 'You have logged out.'}), 200