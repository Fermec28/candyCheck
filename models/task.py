#!/usr/bin/python3
"""
City Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
STORAGE_TYPE = os.environ.get('CANDY_TYPE_STORAGE')


class Task(BaseModel, Base):
    """Task class handles all application tasks"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'tasks'
        title = Column(String(128), nullable=False)
        project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    else:
        state_id = ''
        title = ''
