from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from routes.admin import AdminRoutes
from routes.user import UserRoutes
from routes.auth import AuthRoutes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'anil123'
app.config['MYSQL_DB'] = 'LibraryManagement'

api = Api(app)
jwt = JWTManager(app)

api.add_resource(AdminRoutes, '/admin/<action>')
api.add_resource(UserRoutes, '/user/<action>')
api.add_resource(AuthRoutes, '/auth/<action>')

if __name__ == '__main__':
    app.run(debug=True)
