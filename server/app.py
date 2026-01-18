#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

# --------------------
# CLEAR
# --------------------
class ClearSession(Resource):
    def delete(self):
        session.clear()
        return {}, 204

# --------------------
# SIGNUP
# --------------------
class Signup(Resource):
    def post(self):
        json = request.get_json()

        user = User(username=json['username'])
        user.password_hash = json['password']

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return user.to_dict(), 201

# --------------------
# CHECK SESSION
# --------------------
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if not user_id:
            return {}, 204

        user = User.query.get(user_id)
        if not user:
            return {}, 204

        return user.to_dict(), 200

# --------------------
# LOGIN
# --------------------
class Login(Resource):
    def post(self):
        json = request.get_json()

        user = User.query.filter(
            User.username == json['username']
        ).first()

        if not user:
            return {}, 401

        if not user.authenticate(json['password']):
            return {}, 401

        session['user_id'] = user.id

        return user.to_dict(), 200

# --------------------
# LOGOUT
# --------------------
class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

# --------------------
# ROUTES
# --------------------
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
