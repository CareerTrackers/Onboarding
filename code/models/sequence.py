import sqlite3
from db import db


# Classes
class SequenceModel(db.Model):
  __tablename__ = 'sequences'

  id = db.Column(db.Integer, primary_key = True)
  sequence_name = db.Column(db.String)
  sequence_description = db.Column(db.Text)

  # positions = db.relationship('PositionModel')


  def __init__(self, sequence_name, sequence_description):
    self.sequence_name = sequence_name
    self.sequence_description = sequence_description


  def json(self):
    return {'id': self.id,
            'sequence_name': self.sequence_name,
            'sequence_description': self.sequence_description}


  def json_positions(self):
    # print('*****************')
    # print(self.positions)
    # print('*****************')
    return {'id': self.id,
            'sequence_name': self.sequence_name,
            'sequence_description': self.sequence_description,
            'positions': [position.json_tasks() for position in self.positions]
    }

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(sequence_name = name).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id = _id).first()

  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()


  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
