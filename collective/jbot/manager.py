from zope import interface
import os
import sys
from z3c.jbot import interfaces
from z3c.jbot.manager import find_package
from zope.globalrequest import getRequest
from interfaces import RESOURCE_DIRECTORY_NAME
from zope.component.hooks import getSite
from tempfile import mkdtemp
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory


IGNORE = object()


_file_cache = {}


class Storage(object):

    def __init__(self):
        self.persistent = getUtility(
            IResourceDirectory, name="persistent")[RESOURCE_DIRECTORY_NAME]
        self.directory = self.persistent['custom']
        self.site = getSite()

    def __contains__(self, name):
        return self.directory and name in self.directory

    def get(self, filename, template):
        # get path to file for template
        fi = self.directory[filename]
        tmpdir = mkdtemp()
        tmpfilepath = os.path.join(tmpdir, filename)
        tmpfi = open(tmpfilepath, 'wb')
        tmpfi.write(str(fi.data))
        tmpfi.close()
        return tmpfilepath


_req_cache_key = 'collective.jbot.storage'


class TemplateManager(object):
    interface.implements(interfaces.ITemplateManager)

    def __init__(self, name):
        self.name = name
        self.templates = {}
        self.paths = {}
        self.syspaths = tuple(sys.path)

    def getStorage(self):
        req = getRequest()
        if _req_cache_key not in req.environ:
            req.environ[_req_cache_key] = Storage()
        return req.environ[_req_cache_key]

    def registerTemplate(self, template, token):
        # assert that the template is not already registered
        filename = self.templates.get(token)
        if filename is IGNORE:
            return

        # if the template filename matches an override, we're done
        paths = self.paths
        if paths.get(filename) == template.filename and \
                os.path.exists(filename):
            return

        # verify that override has not been unregistered
        if filename is not None and filename not in paths:
            template.filename = template._filename
            del self.templates[token]

        # check if an override exists
        path = find_package(self.syspaths, template.filename)
        if path is None:
            # permanently ignore template
            self.templates[token] = IGNORE
            return

        filename = path.replace(os.path.sep, '.')

        storage = self.getStorage()
        if filename in storage:
            filepath = storage.get(filename, template)
            self.paths[filename] = filepath

            # save original filename
            template._filename = template.filename

            # save template and registry and assign path
            template.filename = filepath
            self.templates[token] = filename

            return True
