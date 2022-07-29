from marshmallow import fields, validate
from ..config import ma
from ..models import employee_db
from ..config.init import Config


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model       = employee_db
        include_fk  = True
    
    id                  = fields.UUID()
    name                = fields.String(required=True)
    email               = fields.String(required=True)
    password            = fields.String(required=True)
    gender              = fields.Str(required=True, validate=validate.OneOf(["Pria", "Perempuan"]))
    birthdate           = fields.DateTime(format=Config.DATEFORMAT, required=True)

    created_datetime    = fields.DateTime(format=Config.DATETIMEFORMAT, dump_only=True)
    updated_datetime    = fields.DateTime(format=Config.DATETIMEFORMAT, dump_only=True)