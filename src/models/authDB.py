from datetime import datetime
import pytz
import enum
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from ..config import db

class Gender(enum.Enum):
    Pria        = 'Pria'
    Perempuan   = 'Perempuan'

class UserDB(db.Model):
    id                  = db.Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid1)
    name                = db.Column(db.Text(), nullable=False)
    email               = db.Column(db.Text(), nullable=False, unique=True)
    password            = db.Column(db.Text(), nullable=False)
    gender              = db.Column(Enum(Gender))
    birthdate           = db.Column(db.Date(timezone=False), nullable=False)
    
    created_datetime    = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Jakarta')))
    updated_datetime    = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Jakarta')), onupdate=datetime.now(pytz.timezone('Asia/Jakarta')))