from app import api,db
from .common.utils import auth
from flask import abort, make_response
from flask.ext.restful import Resource,reqparse,fields,marshall


"""------------------Fields---------------"""

order_field = {
  
    


}


"""----------------Classes----------------"""

class OrderAPI(Resource):
  decorators = [auth.login_required]
