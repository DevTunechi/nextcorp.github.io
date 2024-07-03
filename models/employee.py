#!/usr/bin/env python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime


class Employee(BaseModel, Base):
    __tablename__ = "employees"
    corp_id = Column(String(60), ForeignKey('corps.id'))
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    passwd = Column(String(128), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    card_id_number = Column(String(128), nullable=False, unique=True)
    phone_number = Column(String(128), nullable=False, unique=True)
    is_hr = Column(Boolean, default=False)
    joined_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    corp_position = Column(String(60), default="None")

    """
    def __init__(self, corp_id, name, email, passwd, birth_date,
                 card_id_number, phone_number, is_hr=False,
                 corp_position=None, joined_date=None, expiry_date=None):
        self.corp_id = corp_id
        self.name = name
        self.email = email
        self.passwd = passwd
        self.birth_date = birth_date
        self.card_id_number = card_id_number
        self.phone_number = phone_number
        self.is_hr = is_hr
        self.corp_position = corp_position
        self.joined_date = joined_date or datetime.utcnow()
        self.expiry_date = expiry_date
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<Employee id={}, name='{}', email='{}'>".format(self.id, self.name, self.email)
