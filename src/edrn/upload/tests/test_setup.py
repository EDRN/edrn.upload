# encoding: utf-8
# Copyright 2014 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

u'''EDRN Upload System — setup tests'''


from edrn.upload.testing import EDRN_UPLOAD_INTEGRATION_TESTING
import unittest2 as unittest

class SetupTest(unittest.TestCase):
    layer = EDRN_UPLOAD_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testSomething(self):
        u'''Ensure something or other works'''
        pass
