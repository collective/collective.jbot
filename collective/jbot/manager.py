from zope import interface
import os
import sys
from z3c.jbot import interfaces
from z3c.jbot.manager import find_package
from zope.globalrequest import getRequest
from interfaces import RESOURCE_DIRECTORY_NAME
from zope.component.hooks import getSite
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
import Globals
from zope.component import ComponentLookupError
from DateTime import DateTime


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
        jbot_dir = os.path.join(Globals.data_dir, 'jbot')
        site_id = self.site.getId()
        if not os.path.exists(jbot_dir):
            os.mkdir(jbot_dir)
        site_jbot_dir = os.path.join(jbot_dir, site_id)
        if not os.path.exists(site_jbot_dir):
            os.mkdir(site_jbot_dir)
        filepath = os.path.join(site_jbot_dir, filename)
        if not os.path.exists(filepath) or \
                DateTime(fi._p_mtime) > DateTime(os.stat(filepath).st_mtime):
            tmpfi = open(filepath, 'wb')
            tmpfi.write(str(fi.data))
            tmpfi.close()
        return filepath


_req_cache_key = 'collective.jbot.storage'


class TemplateManager(object):
    interface.implements(interfaces.ITemplateManager)

    def __init__(self, name):
        self.name = name
        self._req = None
        self.syspaths = tuple(sys.path)

    @property
    def customized_filenames(self):
        key = '%s.%s' % (_req_cache_key, 'customized_filenames')
        if key not in self.req.environ:
            storage = self.storage
            if storage:
                self.req.environ[key] = storage.directory.listDirectory()
            else:
                self.req.environ[key] = []
        return self.req.environ[key]

    @property
    def req(self):
        if self._req is None:
            self._req = getRequest()
        return self._req

    @property
    def paths(self):
        key = '%s.%s' % (_req_cache_key, 'paths')
        if key not in self.req.environ:
            self.req.environ[key] = {}
        return self.req.environ[key]

    @property
    def templates(self):
        key = '%s.%s' % (_req_cache_key, 'templates')
        if key not in self.req.environ:
            self.req.environ[key] = {}
        return self.req.environ[key]

    @property
    def storage(self):
        if _req_cache_key not in self.req.environ:
            try:
                self.req.environ[_req_cache_key] = Storage()
            except ComponentLookupError:
                self.req.environ[_req_cache_key] = None
        return self.req.environ[_req_cache_key]

    def registerTemplate(self, template, token):
        """
        Return True is there has been a change to the override.
        Due to the nature of this implementation, a multi-site deployment
        could cause the template setting of resources to be re-set
        often. This is probably not optimal. And with chamelean I wonder if
        the compiling is re-done each time also... Eek
        """
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

        customized = False
        if hasattr(template, '_filename'):
            # already customized by jbot
            path = find_package(self.syspaths, template._filename)
            customized = True
        else:
            # check if an overridable resource
            path = find_package(self.syspaths, template.filename)
            if path is None:
                # permanently ignore template
                self.templates[token] = IGNORE
                return

        filename = path.replace(os.path.sep, '.')
        # check again if filename in list of cached paths. Might be diff
        # object but some filename, we return a customized version here
        # because one request object corresponds to one site customization
        if filename in self.paths:
            if filename != template.filename:
                if not hasattr(template, '_filename'):
                    template._filename = template.filename
                template.filename = self.paths[filename]
                return True

        if not self.storage:
            if customized:
                # revert now...
                template.filename = template._filename
                del template._filename
                return True
        else:
            if filename in self.customized_filenames:
                filepath = self.storage.get(filename, template)
                if filepath == template.filename:
                    # already customized with correct path, ignore
                    return

                self.paths[filename] = filepath

                # save original filename
                if not hasattr(template, '_filename'):
                    template._filename = template.filename

                # save template and registry and assign path
                template.filename = filepath
                self.templates[token] = filename

                return True
            else:
                if customized:
                    template.filename = template._filename
                    del template._filename
                    return True
