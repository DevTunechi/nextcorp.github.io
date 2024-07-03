#!/usr/bin/env python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Corp(BaseModel, Base):
    __tablename__ = "corps"
    name = Column(String(128), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    passwd = Column(String(128), nullable=False)
    employees = relationship("Employee", backref="corp")
