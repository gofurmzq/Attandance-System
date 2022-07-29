from marshmallow import fields, validate
from ..config import ma
from ..models import UserDB
from ..config.init import Config


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model       = UserDB
        include_fk  = True
    
    id                  = fields.UUID()
    name                = fields.String()
    email               = fields.Email(required=True)
    password            = fields.String(required=True)
    gender              = fields.Str(validate=validate.OneOf(["Pria", "Perempuan"]))
    birthdate           = fields.DateTime(format=Config.DATEFORMAT)

    created_datetime    = fields.DateTime(format=Config.DATETIMEFORMAT, dump_only=True)
    updated_datetime    = fields.DateTime(format=Config.DATETIMEFORMAT, dump_only=True)