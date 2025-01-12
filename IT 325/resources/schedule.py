from flask import request, jsonify
from db import db
from models import Schedule
from schemas import ScheduleSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import create_app

app = create_app()

schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)

@app.route('/schedules', methods=['GET'])
@jwt_required()
def get_all_schedules():
    schedules = Schedule.query.all()
    result = schedules_schema.dump(schedules)
    return jsonify(result), 200

@app.route('/schedules/<int:id>', methods=['GET'])
@jwt_required()
def get_schedule_by_id(id):
    schedule = Schedule.query.get(id)
    if schedule:
        result = schedule_schema.dump(schedule)
        return jsonify(result), 200
    else:
        return {'message': 'Schedule not found'}, 404

@app.route('/schedules/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_schedule_by_user_id(user_id):
    schedules = Schedule.query.filter(Schedule.user_id == user_id).all()
    result = schedules_schema.dump(schedules)
    return jsonify(result), 200

@app.route('/schedules', methods=['POST'])
@jwt_required()
def post_schedule():
  data = request.get_json()
  if not data:
      return {'message': "Invalid data"}, 400
  current_user = get_jwt_identity()
  user_id = data.get('user_id')
  if current_user != user_id:
      return {"message": "Unauthorized action"}, 401
  schedule = schedule_schema.load(data)
  db.session.add(schedule)
  db.session.commit()
  return schedule_schema.dump(schedule), 201

@app.route('/schedules/<int:id>', methods=['PUT'])
@jwt_required()
def put_schedule(id):
    schedule = Schedule.query.get(id)
    if not schedule:
      return {'message': 'Schedule not found'}, 404
    data = request.get_json()
    if not data:
      return {'message': "Invalid data"}, 400
    updated_schedule = schedule_schema.load(data, instance=schedule)
    db.session.commit()
    return schedule_schema.dump(updated_schedule), 200

@app.route('/schedules/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(id):
    schedule = Schedule.query.get(id)
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return {'message': 'Schedule deleted'}, 200
    else:
        return {'message': 'Schedule not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)