#!flask/bin/python

import unittest


loader = unittest.TestLoader()

#tests = loader.discover('.')
tests = loader.discover('SectionTests',pattern = 'test*.py')

runner = unittest.TextTestRunner()

runner.run(tests)





