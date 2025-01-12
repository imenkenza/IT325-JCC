"""from marshmallow import Schema, fields
#class CourseitemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Float(required=True)
    specialization_id = fields.Str(required=True)
class CourseitemUpdateSchema(Schema):
    name = fields.Str()
    type = fields.Float()
class SpecializationSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True) """

from marshmallow import Schema, fields

class PlainCourseItemSchema(Schema):
    course_item_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    specialization_id = fields.Int(required=True)

class PlainSpecializationSchema(Schema):
    specialization_id = fields.Int(dump_only=True)
    name = fields.Str()

class CourseItemSchema(PlainCourseItemSchema):
    specialization_id = fields.Int(required=True, load_only=True)
    specialialization = fields.Nested(PlainSpecializationSchema(), dump_only=True)

class CourseItemUpdateSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)

class SpecializationSchema(PlainSpecializationSchema):
    courseitems = fields.List(fields.Nested(PlainCourseItemSchema()), dump_only=True)
