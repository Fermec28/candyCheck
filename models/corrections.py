#!/usr/bin/python3
"""
State Class from Models Module
"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
STORAGE_TYPE = os.environ.get('CANDY_TYPE_STORAGE')


class Correction(BaseModel, Base):
    """Correction class handles all application correction"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'correction'
        status = Column(String(10), nullable=False)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
        project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
        checks = relationship('Check', backref='correction', cascade='delete')
    else:
        status = ''

        @property
        def checks(self):
            """
                getter method, returns list of Check objs from storage
                linked to the current State
            """
            check_list = []
            for check in models.storage.all("Check").values():
                if check.project_id == self.id:
                    check_list.append(check)
            return check_list
