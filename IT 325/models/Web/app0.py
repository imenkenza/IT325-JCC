#Checked
from flask import Flask
from flask import request
import uuid
from db import specializations , course_items
from flask import abort

app = Flask(__name__)
#specializations = [{"name": "IT", "course_items": [{"name": "Web Services", "Type": "Mandatory"}]}]

#checked
#updated
@app.get("/course_item/<string:course_item_id>")
#def get_course_item_in _specializations
def get_course_item(course_item_id):
    try:
        return course_items[course_item_id]
    except KeyError:
        abort(404,message="course item not found")
        #return {"message":"course item not found"},404   

#checked
#updated
@app.post("/course_item")
def create_course_item():
    course_item_data = request.get_json()
    #if course_item_data["specialization_id"] not in specializations:
       # abort(404, message="specialization not found")
        #return {"message": "Specialization not found"}, 404
    if(
        "type" not in course_item_data
        or "specialization_id" not in course_item_data
        or "name" not in course_item_data
    ):
        abort(404, message="Bad request. Ensure 'type','id' and 'name' are included in the json file")
    for course_item in course_items.values():
        if (course_item_data["name"]==course_item["name"]
            and course_item_data["specialization_id"]==course_item["specilization_id"]):
            abort(400,message="This course item already exists.")
    course_item_id=uuid.uuid4().hex
    course_item={**course_item_data,"id":course_item_id}
    course_items[course_item_id]=course_item
    return course_item, 201
    #for specialization in specializations:
        #if specialization["name"] == name:
            #new_course_item = {"name": request_data["name"], "type": request_data["type"]}
            #specialization["course_items"].append(new_course_item)
            #return new_course_item, 201
        #return {"message": "Specialization not found"}, 404

#added & checked
@app.delete("/course_item/<string:course_item_id>")
def delete_course_item(course_item_id):
    try:
        del course_items[course_item_id]
        return {"message": "Course_item deleted."}
    except KeyError:
        abort(404, message="Course_item not found.")

#added & checked
@app.put("/course_item/<string:course_item_id>")
def update_course_item(course_item_id):
    course_item_data = request.get_json()
    if "type" not in course_item_data or "name" not in course_item_data:
        abort(400,message="Bad request. Ensure 'type', and 'name' are included in the JSON payload.",)
    try:
        course_item = course_items[course_item_id]
        course_item |= course_item_data
        return course_item
    except KeyError:
        abort(404, message="Course_item not found.")

#checked
#newly added 
@app.get("/course_item")
def get_all_course_items():
    return {"course_items": list(course_items.values())}

#checked
@app.get("/specialization/string:<specialization_id>")
def get_specialization(specialization_id):
    try:
        # Here you might also want to add the course_items in this specialization
        # We'll do that later on in the course
        return specializations[specialization_id]
    except KeyError:
        abort(404,message="specialization not found")
        #return {"message":"specialization not found"},404   
    #for specialization in specializations:
        #if specialization["name"] == name:
            #return specialization
        #return {"message": "Specialization not found"}, 404

#checked
#updated
@app.post("/specialization")
def create_specialization():
    specialization_data= request.get_json()
    if "name" not in specialization_data:
        abort(400, message="Bad Request. Ensure 'name' is included in the Json file")
    for specialization in specializations.values():
        if specialization_data["name"] == specialization["name"] :
            abort(400, message="Specialization already exists")  
    specialization_id = uuid.uuid4().hex
    specialization= {**specialization_data,"id":specialization_id}
    #request_data = request.get_json()
    #new_specialization ={"name": request_data["name"], "course_items": []}
    #specializations.append(new_specialization)
    #return specialization, 201 
    specializations[specialization_id] = specialization
    return specialization

#checked
@app.delete("/specialization/<string:specialization_id>")
def delete_specialization(specialization_id):
    try:
        del specializations[specialization_id]
        return {"message": "Specialization deleted."}
    except KeyError:
        abort(404, message="Specialization not found.")

#checked
@app.get("/specialization")
def get_specializations():
    return {"specializations": list(specializations.values())}



#to make sure that we will run only this oython file even after importing other ones
if __name__ == "__main__":
    app.run(debug=True)