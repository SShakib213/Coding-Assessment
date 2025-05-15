from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key' 

jwt = JWTManager(app)

users_db = {}  # Simulated in-memory database

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users_db:
        return jsonify({'msg': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    users_db[username] = hashed_password

    return jsonify({'msg': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    stored_password = users_db.get(username)
    if not stored_password or not check_password_hash(stored_password, password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    token = create_access_token(identity=username)
    return jsonify({'token': token}), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'msg': f'Hello {current_user}, you are authorized!'}), 200

if __name__ == '__main__':
    app.run(debug=True)

