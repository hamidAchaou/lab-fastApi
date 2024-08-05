from marshmallow import Schema, fields

class UserCreateSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    full_name = fields.Str(required=True)
    password = fields.Str(required=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class SuiviSchema(Schema):
    id = fields.Int()
    # Define other fields similarly

class VilleSchema(Schema):
    id = fields.Int()
    nom = fields.Str()

class TypeBienSchema(Schema):
    id = fields.Int()
    nom = fields.Str()

class StatutSchema(Schema):
    id = fields.Int()
    nom = fields.Str()
