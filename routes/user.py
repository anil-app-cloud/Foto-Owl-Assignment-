from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import mysql

class UserRoutes(Resource):
    @jwt_required()
    def get(self, action):
        if action == 'books':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM Books")
            books = cursor.fetchall()
            return jsonify({"books": books})
    
    @jwt_required()
    def post(self, action):
        if action == 'request':
            user = get_jwt_identity()
            data = request.get_json()
            book_id, start_date, end_date = data.get('book_id'), data.get('start_date'), data.get('end_date')
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO BorrowRequests (user_id, book_id, start_date, end_date)
                VALUES (%s, %s, %s, %s)
            """, (user['user_id'], book_id, start_date, end_date))
            mysql.connection.commit()
            return jsonify({"message": "Request submitted"})
