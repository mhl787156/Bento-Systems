#!flask/bin/python

import unittest

from SectionTests.xmlTestrunner import XMLTestRunner

loader = unittest.TestLoader()

#tests = loader.discover()
tests = loader.discover('SectionTests',pattern = 'test*.py')

runner = XMLTestRunner()

runner.run(tests)





