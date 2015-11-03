from app import api,db
from app.common.utils import auth
from flask import abort, make_response,jsonify
from flask.ext.restful import Resource,reqparse,fields
from app.models import User,MenuItem,OrderItem,OrderCounter,Order


"""------------------Fields---------------"""

order_field = {
  
    


}


"""----------------Classes----------------"""
class OrderAPI(Resource):
  #decorators = [auth.login_required]
  def get(self,data=None):
    #returns order number 'data'
    return { 'hello' : 'world' +str(data)}

  def post(self,data):
    #edits a current order into the system
    return "put {} in db".format(data)

  def delete(self,data):
    # 'deletes' current order
    return

class NewOrderAPI(Resource):
  #decorators = [auth.login_requried]
  def get(self):
    return 
  def post(self):
    return

class OrderEditAPI(Resource):
  #decorators = [auth.login_requried]
  def get(self):
    return 
  def post(self):
    return
  def delete(self):
    return

