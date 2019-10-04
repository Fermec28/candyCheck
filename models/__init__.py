import os
from models.base_model import BaseModel
from models.user import User
from model.projects import Project
from models.task import Task
from models.corrections import Correction
from models.check import Check

"""CNC - dictionary = { Class Name (string) : Class Type }"""

if os.environ.get('CANDY_TYPE_STORAGE') == 'db':
    from models.engine import db_storage
    CNC = db_storage.DBStorage.CNC
    storage = db_storage.DBStorage()
else:
    from models.engine import file_storage
    CNC = file_storage.FileStorage.CNC
    storage = file_storage.FileStorage()

storage.reload()
