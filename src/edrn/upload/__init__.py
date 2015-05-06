# encoding: utf-8
# Copyright 2014 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

u'''EDRN — Upload System'''

from zope.i18nmessageid import MessageFactory

PACKAGE_NAME = __name__
MESSAGE_FACTORY = MessageFactory(PACKAGE_NAME)
DEFAULT_PROFILE = u'profile-' + PACKAGE_NAME + ':default'
