import enum 
import datetime as dt
import pytz
import uuid
from sqlalchemy import Enum 
from sqlalchemy.dialects.postgresql import UUID 
from .authDB import *
from ..config import db 

class Status(enum.Enum):
    IN_QUEUE    = 'IN_QUEUE'
    DONE        = 'DONE'
    CANCELLED   = 'CANCELLED'

class ActivityDB(db.Model):
    id                  = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    user_id         = db.Column(UUID(as_uuid=True), db.ForeignKey(UserDB.id), nullable=False)
    date                = db.Column(db.Date())
    check_in            = db.Column(db.Time())
    activity            = db.Column(db.Text(), nullable=True)
    status              = db.Column(Enum(Status))
    check_out           = db.Column(db.Time())
    
    created_datetime    = db.Column(db.DateTime(timezone=True), default=dt.datetime.now(pytz.timezone('Asia/Jakarta')))
    updated_datetime    = db.Column(db.DateTime(timezone=True), default=dt.datetime.now(pytz.timezone('Asia/Jakarta')), onupdate=dt.datetime.now(pytz.timezone('Asia/Jakarta')))
    
    employee            = db.relationship('UserDB', backref='activity', lazy=True)