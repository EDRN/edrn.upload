# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Acquisition import aq_inner
from edrn.upload import MESSAGE_FACTORY as _
from edrn.upload.dataset import IDataset
from five import grok
from plone.memoize.instance import memoize
from plone.supermodel import model
from Products.CMFCore import permissions
from zope import schema
import plone.api

class IDatasetFolder(model.Schema):
    u'''A container for datasets.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Name of this dataset folder.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this folder.'),
        required=False,
    )
    filesystemPath = schema.TextLine(
        title=_(u'Filesystem Path'),
        description=_(u'Where on the local filesystem this data resides.'),
        required=True,
    )


class View(grok.View):
    u'''View for a dataset folder'''
    grok.context(IDatasetFolder)
    grok.require('zope2.View')
    @memoize
    def datasets(self):
        context = aq_inner(self.context)
        catalog = plone.api.portal.get_tool('portal_catalog')
        return catalog(
            object_provides=IDataset.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
    def numDatasets(self):
        return len(self.datasets())
    def showAddDatasetButton(self):
        context = aq_inner(self.context)
        portalMembership = plone.api.portal.get_tool('portal_membership')
        return portalMembership.checkPermission(permissions.AddPortalContent, context)
    def addDatasetURL(self):
        context = aq_inner(self.context)
        return context.absolute_url() + u'/++add++edrn.upload.dataset'
