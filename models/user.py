#!/usr/bin/python3
"""
User Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
STORAGE_TYPE = os.environ.get('CANDY_TYPE_STORAGE')


class User(BaseModel, Base):
    """
        User class handles all application users
    """
    if STORAGE_TYPE == "db":
        __tablename__ = 'users'
        name = Column(String(128), nullable=True)

    else:
        name = ''

    def __init__(self, *args, **kwargs):
        """
            instantiates user object
        """
        super().__init__(*args, **kwargs)
