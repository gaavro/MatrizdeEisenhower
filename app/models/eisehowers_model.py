from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import relationship

@dataclass
class Eisehowers(db.Model):
    id:int
    type:str
    __tablename__ = 'eisehowers'


    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    
    tasks = relationship('Tasks', backref='eisehowers_classification')
   


