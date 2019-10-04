#!/usr/bin/python3
"""
State Class from Models Module
"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
STORAGE_TYPE = os.environ.get('CANDY_TYPE_STORAGE')


class Project(BaseModel, Base):
    """Project class handles all application states"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'projects'
        name = Column(String(128), nullable=False)
        tasks = relationship('Task', backref='projects', cascade='delete')
    else:
        name = ''

        @property
        def tasks(self):
            """
                getter method, returns list of Task objs from storage
                linked to the current State
            """
            task_list = []
            for task in models.storage.all("Task").values():
                if task.project_id == self.id:
                    task_list.append(task)
            return task_list
