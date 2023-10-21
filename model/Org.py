from base import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class Org(db.Model):
    __tablename__ = "org"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.SmallInteger, primary_key=True)
    case_level1_key = db.Column(UUID)
    short_name = db.Column(db.String)
    date_update = db.Column(db.DateTime(), default=datetime.now())
