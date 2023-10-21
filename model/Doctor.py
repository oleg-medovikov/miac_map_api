from base import db


class Doctor(db.Model):
    __tablename__ = "doctor"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.SmallInteger, primary_key=True)
    org = db.Column(db.String)
    fio = db.Column(db.String(200))
    snils = db.Column(db.BigInteger, nullable=True)
    telefon = db.Column(db.String(20), nullable=True)
    spec = db.Column(db.String, nullable=True)
