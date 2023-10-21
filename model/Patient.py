from base import db
from sqlalchemy.dialects.postgresql import UUID


class Patient(db.Model):
    __tablename__ = "patient"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    # глобальный идентификатор
    global_id = db.Column(UUID)
    sex = db.Column(db.Boolean)
    # дата рождения
    birthdate = db.Column(db.Date)
    birthdate_baby = db.Column(db.Date, nullable=True)
