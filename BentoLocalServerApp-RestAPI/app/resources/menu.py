from app import api,db
from app.common.utils import auth
from flask import abort, make_response,jsonify
from flask.ext.restful import Resource,reqparse,fields
from app.models import User,Menu,MenuSection,MenuItem


"""------------------Fields---------------"""

  
    



"""----------------Classes----------------"""
class MenuAPI(Resource):
  #decorators = [auth.login_required]
  def get(self,data=None):
    q = Menu.query
    if data!=None:
      q = q.filter_by(id=data)
    return jsonify(json_list = [i.serialize() for i in q.all()])

class MenuItemAPI(Resource):
  #decorators = [auth.login_required]
  def get(self,data=None):
    q = MenuItem.query
    if data!=None:
      q = q.filter_by(id=data)
    return jsonify(json_list = [i.serialize() for i in q.all()])

class MenuSectionAPI(Resource):
  #decorators = [auth.login_required]
  def get(self,data=None):
    q = MenuSection.query
    if data!=None:
      q = q.filter_by(id=data)
    return jsonify(json_list = [i.serialize() for i in q.all()])

