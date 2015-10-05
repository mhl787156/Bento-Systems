from resources.order import OrderAPI

def add_all_resources(api):
  api.add_resource(OrderAPI,'/order')
