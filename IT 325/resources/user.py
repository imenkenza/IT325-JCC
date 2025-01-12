from flask import request, jsonify
from db import db
from models import User
from schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from flask_mail import Mail, Message
from db import create_app
from flask import current_app

app = create_app()
mail = Mail(app)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def send_confirmation_email(email, token):
  msg = Message("Confirm Registration", recipients=[email])
  msg.body = f"Your confirmation token: {token}"

  try:
    mail.send(msg)
    return True
  except Exception as e:
    print(e)
    return False

@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  if not data:
    return {'message': "Invalid data"}, 400

  try:
    validate_email(data['email'])
  except EmailNotValidError as e:
    return {"message": "Invalid email format", "error": str(e)}, 400

  username = data.get('username')
  email = data.get('email')
  password = data.get('password')

  user_exist = User.query.filter_by(username=username).first()
  if user_exist:
    return {'message': 'Username already exist'}, 409

  email_exist = User.query.filter_by(email=email).first()
  if email_exist:
      return {'message': 'Email already exist'}, 409

  hashed_password = generate_password_hash(password)

  new_user = User(username=username, email=email, password=hashed_password)

  db.session.add(new_user)
  db.session.commit()

  token = create_access_token(identity=new_user.id)
  send_confirmation_email(email, token)
  return {'message': "User Created Successfully. Please check your email for confirmation token", 'token':token}, 201

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  if not data:
      return {'message': "Invalid data"}, 400

  username = data.get('username')
  password = data.get('password')

  user = User.query.filter_by(username=username).first()
  if user and check_password_hash(user.password, password):
      token = create_access_token(identity=user.id)
      return {'token': token, "message": "Logged in successfuly"}, 200
  else:
      return {'message': "Invalid username or password"}, 401

@app.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result), 200

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        result = user_schema.dump(user)
        return jsonify(result), 200
    else:
        return {'message': 'User not found'}, 404

@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user_by_id(id):
    current_user = get_jwt_identity()
    if current_user != id :
      return {"message": "Unauthorized action"}, 401
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200
    else:
        return {'message': 'User not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)