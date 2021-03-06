# import libraries
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

from resources.task import Task, Tasks
from resources.sequence import Sequence, Sequences, TaskList
from resources.position import Position, Positions
from resources.user import User, Users
from resources.template import Template, Templates
from resources.set import Set, Sets, AddSequence


from dotenv import load_dotenv
from resources.google_login import (
  GoogleLogin, 
  GoogleAuthorize, 
  GoogleLogout, 
  GetCurrentUser)


from config import DefaultConfig

# Configs & initialisations
load_dotenv(".env")
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(DefaultConfig)
app.permanent_session_lifetime = timedelta(minutes=5)

api = Api(app)
jwt = JWTManager(app)

# Endpoints
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/user/<string:userid>')

api.add_resource(Tasks, '/api/tasks')
api.add_resource(Task,  '/api/task')

api.add_resource(Positions, '/positions')
api.add_resource(Position,  '/position')

api.add_resource(Templates, '/api/templates')
api.add_resource(Template, '/api/template')

api.add_resource(Sets, '/api/sets')
api.add_resource(Set, '/api/set')
api.add_resource(AddSequence, '/addsequence/<int:set_id>')

api.add_resource(Sequences, '/api/sequences')
api.add_resource(Sequence,  '/api/sequence/<int:_id>')
api.add_resource(TaskList, '/api/tasklist/<int:set_id>')

api.add_resource(GoogleLogin, "/login/google")
api.add_resource(GoogleAuthorize, "/login/google/authorized", endpoint = "google.authorize")
api.add_resource(GetCurrentUser, "/api/getcurrentuser")
api.add_resource(GoogleLogout, "/api/logout")


# Main
if __name__ == '__main__':
  from db import db
  db.init_app(app)
  app.run(port = 5000, debug = True)

