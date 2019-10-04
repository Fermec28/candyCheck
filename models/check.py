#!/usr/bin/python3
"""
Check Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
STORAGE_TYPE = os.environ.get('CANDY_TYPE_STORAGE')


class Check(BaseModel, Base):
    """Check class handles all application tasks"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'check'
        title = Column(String(128), nullable=False)
        passed = Column(String(6), nullable=False)
        correction_id = Column(Integer, ForeignKey('correction.id'), nullable=False)
    else:
                title = ''
                passed = 0
