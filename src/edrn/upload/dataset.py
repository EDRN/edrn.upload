# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Acquisition import aq_inner
from datetime import datetime
from edrn.upload import MESSAGE_FACTORY as _
from five import grok
from plone.memoize.instance import memoize
from plone.supermodel import model
from zope import schema
import anyjson, os, os.path, urllib, urlparse


class IDataset(model.Schema):
    u'''A dataset has some metadata attributes and a bunch of files.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Name of this dataset.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'An abstract about this data.'),
        required=False,
    )
    principalInvestigator = schema.TextLine(
        title=_(u'Principal Investigator'),
        description=_(u'Name of the PI whose project generated this dataset.'),
        required=False,
    )
    siteName = schema.TextLine(
        title=_(u'Site Name'),
        description=_(u'Name of the institution that produced this dataset.'),
        required=False,
    )
    curationDate = schema.Date(
        title=_(u'Curation Date'),
        description=_(u'Date this dataset was first curated.'),
        required=False,
    )
    metadata1 = schema.TextLine(
        title=_(u'Metadata 1'),
        description=_(u'Some bit of other metadata.'),
        required=False,
    )
    metadata2 = schema.TextLine(
        title=_(u'Metadata 2'),
        description=_(u'Another bit of metadata.'),
        required=False,
    )
    

class View(grok.View):
    u'''View for a dataset'''
    grok.context(IDataset)
    grok.require('zope2.View')
    def uploadURL(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        path = urlparse.urlparse(url).path + u'/@@upload'
        return u'var edrnUploadURL = "{}";'.format(path)
    def numFiles(self):
        return len(self.currentFiles())
    @memoize
    def currentFiles(self):
        context = aq_inner(self.context)
        baseURL = context.absolute_url() + u'/@@retrieve?name='
        d = context.filesystemPath + u'/' + unicode(context.id)
        if not os.path.exists(d):
            os.makedirs(d)
        entries = os.listdir(d)
        entries.sort()
        files = []
        for entry in entries:
            path = os.path.join(d, entry)
            if os.path.isfile(path):
                mtime = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
                url = baseURL + urllib.quote(entry)
                files.append(dict(name=entry, size=os.path.getsize(path), mtime=mtime, url=url))
        return files


class DataAcceptor(grok.View):
    u'''Accepts data uploaded to a dataset'''
    grok.context(IDataset)
    grok.require('cmf.ModifyPortalContent')
    grok.name('upload')
    def render(self):
        self.request.response.setHeader('Content-type', 'application/json; charset=utf-8')
        context = aq_inner(self.context)
        d = context.filesystemPath + u'/' + unicode(context.id)
        if not os.path.exists(d):
            os.makedirs(d)
        form = self.request.form
        if 'name' not in form or 'file' not in form:
            return anyjson.serialize({u'OK': 0, u'info': u'Missing "name" and/or "file" form elements'})
        name, infile = form['name'], form['file']
        target = os.path.join(d, name)
        with open(target, 'wb') as outfile:
            while True:
                buf = infile.read(512)
                if len(buf) == 0: break
                outfile.write(buf)
        return anyjson.serialize({u'OK': 1})


class DataRetriever(grok.View):
    u'''Retrieves a file from a dataset'''
    grok.context(IDataset)
    grok.require('zope2.View')
    grok.name('retrieve')
    def render(self):
        context = aq_inner(self.context)
        d = context.filesystemPath + u'/' + unicode(context.id)
        if not os.path.exists(d):
            os.makedirs(d)
        if 'name' not in self.request.form:
            raise ValueError(u'Required parameter "name" missing')
        name = self.request.form['name']
        path = os.path.join(d, name)
        if not os.path.isfile(path):
            self.request.response.setStatus(404, u'File {} not found'.format(name))
        self.request.response.setStatus(200, u'OK')
        self.request.response.setHeader(u'Content-type', u'application/octet-stream')
        self.request.response.setHeader(u'Content-length', unicode(os.path.getsize(path)))
        self.request.response.setHeader(u'Content-disposition', u'attachment; filename={}'.format(name))
        with open(path, 'rb') as infile:
            while True:
                buf = infile.read(512)
                if len(buf) == 0: break
                self.request.response.write(buf)
