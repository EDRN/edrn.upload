EDRN Upload System
==================

To demonstrate the EDRN Upload System, we'll classes in a series of functional
tests. And to do so, we'll need a test browser::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

This browser has full manager permissions, but we'll need a plain browser to
test some of the more user-level functions::

    >>> userBrowser = Browser(app)

Let's go.


Uploader
========

An "Uploader" is an object in the site which allows files to be uploaded.  It
can exist anywhere in the site.  Let's make one::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='edrn-upload-uploader')
    >>> l.url.endswith('++add++edrn.upload.uploader')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'Test Uploader 1'
    >>> browser.getControl(name='form.widgets.description').value = u'Just for functional testing.'
    >>> browser.getControl(name='form.buttons.save').click()




