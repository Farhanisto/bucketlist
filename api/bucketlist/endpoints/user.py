import logging

from flask import request, jsonify, make_response
from flask_restplus import Resource
from api.bucketlist.serializers import user
from api.restplus import api
from models import db
from models.models import User,BlacklistToken

log = logging.getLogger(__name__)
ns = api.namespace("auth", description="user registration")


@ns.route('/register')
class RegisterAPI(Resource):
    @api.expect(user)
    def post(self):
        """
            User Registration Resource
            """
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(username=post_data.get('username')).first()
        if not user:
            try:
                user = User(
                    username=post_data.get('username'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject), 201)
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject), 202)


@ns.route('/login')
class LoginAPI(Resource):
    @api.expect(user)
    def post(self):
        """
            User Login Resource
            """
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                username=post_data.get('username')
              ).first()
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return responseObject, 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject), 401)

@ns.route('/status')
@api.header("Authorization", "JWT Token", required=True)
class UserAPI(Resource):
    """
    User Resource
    """
    def get(self):
        """get the status of the user"""
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header:
            resp = User.decode_auth_token(auth_header)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,

                    }
                }
                return responseObject, 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return responseObject, 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return responseObject, 401


@ns.route("/logout")
@api.header("Authorization", "JWT Token", required=True)
class logoutApi(Resource):
    def post(self):
        """Logout"""
        access_token = request.headers.get('Authorization')
        if access_token:
            resp = User.decode_auth_token(access_token)
            if not isinstance(resp, str):
                blacklist_token = BlacklistToken(token=access_token)
                try:
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response_object = {
                        'status': "success",
                        'message': "successfully logged out."
                    }
                    return response_object, 200
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return response_object, 403
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'please login'
                }
                return response_object, 401

        else:
            response_object={
                'status': 'fail',
                'message': 'please login'
            }
            return response_object, 403






