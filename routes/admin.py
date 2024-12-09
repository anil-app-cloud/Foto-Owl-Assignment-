from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models import mysql

class AdminRoutes(Resource):
    @jwt_required()
    def get(self, action):
        if action == 'requests':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM BorrowRequests")
            requests = cursor.fetchall()
            return jsonify({"requests": requests})
    
    @jwt_required()
    def post(self, action):
        if action == 'approve':
            data = request.get_json()
            request_id = data.get('request_id')
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE BorrowRequests SET status = 'Approved' WHERE request_id = %s", (request_id,))
            mysql.connection.commit()
            return jsonify({"message": "Request approved"})
