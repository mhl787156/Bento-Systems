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
    return { 'hello' : 'world' +str(data)}

  def put(self,data):
    return "put {} in db".format(data)

  def delete(self,data):
    return

  def post(self,data):
    return
