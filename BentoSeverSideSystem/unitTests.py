#!flask/bin/python

import unittest
import test_login


def allSuites():
  suites = [
             loginTests.suite()
           ]

  return unittest.TestSuite(suites)









