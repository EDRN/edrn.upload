# encoding: utf-8
# Copyright 2014 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

u'''EDRN Upload System — Testing layers and fixtures.'''

from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting, PLONE_FIXTURE

class EDRNUploadLayer(PloneSandboxLayer):
    u'''Testing layer for EDRN upload system'''
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        super(EDRNUploadLayer, self).setUpZope(app, configurationContext)
        import edrn.upload
        self.loadZCML(package=edrn.upload)
    def setUpPloneSite(self, portal):
        super(EDRNUploadLayer, self).setUpPloneSite(portal)
        self.applyProfile(portal, 'edrn.upload:default')

EDRN_UPLOAD = EDRNUploadLayer()
EDRN_UPLOAD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDRN_UPLOAD,),
    name='EDRNUploadLayer:Integration'
)
EDRN_UPLOAD_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDRN_UPLOAD,),
    name='EDRNUploadLayer:Functional'
)
