from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from models import mysql

class AuthRoutes(Resource):
    def post(self, action):
        if action == 'login':
            data = request.get_json()
            email, password = data.get('email'), data.get('password')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT user_id, password FROM Users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user[1], password):
                access_token = create_access_token(identity={'user_id': user[0], 'email': email})
                return jsonify({"token": access_token})
            return jsonify({"message": "Invalid credentials"}), 401
        elif action == 'register':
            data = request.get_json()
            email, password = data.get('email'), data.get('password')
            hashed_password = generate_password_hash(password)
            cursor = mysql.connection.cursor()
            try:
                cursor.execute("INSERT INTO Users (email, password) VALUES (%s, %s)", (email, hashed_password))
                mysql.connection.commit()
                return jsonify({"message": "User registered successfully"})
            except:
                return jsonify({"message": "Email already exists"}), 400
