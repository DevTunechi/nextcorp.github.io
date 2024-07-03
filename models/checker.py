#!/usr/bin/env python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class CheckInOut(BaseModel, Base):
    __tablename__ = "checkinsouts"
    user_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
    checkin = Column(DateTime, nullable=False)
    checkout = Column(DateTime)
    user = relationship("Employee", backref="checkinsouts")
