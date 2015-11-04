from app import api,db
from app.common.utils import auth
from flask import abort, make_response,jsonify,url_for
from flask.ext.restful import Resource,reqparse,fields,marshal
from app.models import User,MenuItem,OrderItem,OrderCounter,Order


"""------------------Fields---------------"""

order_field = {
  
    


}

new_order_fields = {
  'id' : fields.Integer,
  'table_number' : fields.Integer,
  'number_of_customers' : fields.Integer,
  'staggered_service_order' : fields.Integer,
  'uri' : fields.String #fields.Url('neworder')
}


"""----------------Classes----------------"""
class OrderAPI(Resource):
  #decorators = [auth.login_required]

  def get(self,data=None):
    #returns order number 'data'
    return { 'hello' : 'world' +str(data)}

  def delete(self,data):
    # 'deletes' current order
    return

class NewOrderAPI(Resource):
  #decorators = [auth.login_requried]

  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('table_number',type=int,location='json')
    self.reqparse.add_argument('number_of_customers',type=int,location='json')
    self.reqparse.add_argument('staggered_service_order',type=int,location='json')
    super(NewOrderAPI, self).__init__()

  def post(self):
    # Generates a new Order from the data given
    args = self.reqparse.parse_args()
    
    newOrder = Order(args['table_number'], 
                     args['number_of_customers'], 
                     args['staggered_service_order'])

    db.session.add(newOrder)
    db.session.commit()

    serial = newOrder.serialize()
    serial['uri'] = url_for('order',data=newOrder.id,_external=True)
                     
    return { 'new_order' : marshal( serial ,new_order_fields) } 

class OrderEditAPI(Resource):
  #decorators = [auth.login_requried]
  def post(self,orderID,data):
    # Add a new item data to an order orderID
    return
  def delete(self,orderID,data):
    # Removes item data if it exists in order orderID
    return

