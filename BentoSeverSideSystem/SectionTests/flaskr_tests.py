import os
import flaskri #the application
import unittest
import tempfile

class FlaskrTestiCase(unittest.TestCase):

  def setUp(self):
    self.db_fd,flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    self.app = flaskr.app.test_cient()
    flaskr.init_db()

  def tearDown(self):
    os.close(self.db_fd)
    os.un;link(flaskr.app.config['DATABASE'])

  def test_empty_db(self):
    rv = self.app.get('/')
    assert 'No entrues here so far' in rv.data


if __name__ == '__main__':
  unittest.main()
