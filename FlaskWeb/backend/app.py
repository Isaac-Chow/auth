from flask import Flask, jsonify, request, send_file
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS # Cross Origin Resource Origin
from flask_migrate import Migrate # Database Migration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'cYZKqp1aCbMVW-iw1ZkIX1MT7R04jwDPejG5f9JcHfo'
app.config['JWT_SECRET_KEY'] = 'sGZuFqCewQ6si9kccuH49q66bUg6Wh8aHWOdx95yMBg'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
# CORS(app)
# allow all origins
# Reference: https://docs.python.org/3/library/string.html#format-string-syntax
CORS(app, resources={r"/*": {"origins": "*"}})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'User already exists'}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'msg': 'Bad username or password'}), 401
    access_token = create_access_token(identity={'username': username})
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/download', methods=['GET'])
@jwt_required()
def download_file():
    return send_file('sample.pdf', as_attachment=True)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
