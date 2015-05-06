# encoding: utf-8
# Copyright 2014–2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Acquisition import aq_inner
from edrn.upload import MESSAGE_FACTORY as _
from five import grok
from plone.supermodel import model
from zope import schema
import anyjson


class IUploader(model.Schema):
    u'''An uploader'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Name of this uploader.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this uploader.'),
        required=False,
    )


class View(grok.View):
    u'''View for an uploader'''
    grok.context(IUploader)
    grok.require('zope2.View')

    def getUploadURLJavascript(self):
        u'''Yield the Javascript that tells where the upload API lives for an uploader'''
        context = aq_inner(self.context)
        return u'var uploadURL = "{}/@@upload";'.format(context.absolute_url())


class DataAcceptor(grok.View):
    u'''Accepts data uploaded to an uploader'''
    grok.context(IUploader)
    grok.require('cmf.ModifyPortalContent')
    grok.name('upload')

    def render(self):
        self.request.response.setHeader('Content-type', 'application/json; charset=utf-8')
        return anyjson.serialize({u'OK': u'1'})
