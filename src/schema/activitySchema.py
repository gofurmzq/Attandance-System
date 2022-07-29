from marshmallow import fields, validate
from ..config import ma
from ..models import activityDB
from ..config.init import Config


class ActivitySchema(ma.SQLAlchemySchema):
    class Meta:
        model       = activityDB
        include_fk  = True
    
    id                  = fields.UUID()
    employee_id         = fields.UUID()
    date                = fields.DateTime(format=Config.DATEFORMAT, required=True)
    check_in            = fields.DateTime(format=Config.TIMEFORMAT)
    activity            = fields.String()
    status              = fields.Str(validate=validate.OneOf(["IN_QUEUE","DONE","CANCELLED"]))
    check_out           = fields.DateTime(format=Config.TIMEFORMAT)

    created_datetime    = fields.DateTime(format=Config.DATETIMEFORMAT, dump_only=True)
    updated_datetime    = fields.DateTime(format=Config.DATETIMEFORMAT, dump_only=True)
    
    