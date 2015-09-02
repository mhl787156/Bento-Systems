from app import auth,models

@auth.verify_password
def verify_pw(device_id,password):
  device = models.Device.query.get('device_id'==device_id)
  return device.check_password(password)

@auth.error_handler
def unauthorised():
  return 403
