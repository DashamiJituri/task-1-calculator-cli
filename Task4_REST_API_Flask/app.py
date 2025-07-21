from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store
users = {}

# Create a user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = data.get('id')
    users[user_id] = data
    return jsonify({"message": "User created", "user": data}), 201

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Read a single user
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# Update a user
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    users[user_id] = data
    return jsonify({"message": "User updated", "user": data})

# Delete a user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)


