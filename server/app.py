from flask import Flask, jsonify, request
from models import Session, User

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def get_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.close()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
def create_user():
    session = Session()
    user = User(name=request.json['name'], age=request.json['age'], email=request.json['email'])
    session.add(user)
    session.commit()
    session.close()
    return jsonify(user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    if user is None:
        session.close()
        return jsonify({'error': 'User not found'}), 404
    user.name = request.json.get('name', user.name)
    user.age = request.json.get('age', user.age)
    user.email = request.json.get('email', user.email)
    session.commit()
    session.close()
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    if user is None:
        session.close()
        return jsonify({'error': 'User not found'}), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify({'message': 'User deleted'})

if __name__ == "__main__":
    app.run(debug=True)