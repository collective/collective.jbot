from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.FSObject import FSObject
import json
from plone.app.customerize.registration import templateViewRegistrations
from five.customerize.utils import findViewletTemplate
from five.customerize.interfaces import ITTWViewTemplate
from zope.component import getMultiAdapter
from AccessControl import Unauthorized
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from collective.jbot.interfaces import RESOURCE_DIRECTORY_NAME


def mangleAbsoluteFilename(filename):
    parts = filename.split('/')
    pivot = 0
    for idx, part in enumerate(reversed(parts[:-2])):
        if '.' in part:
            pivot = idx
            break
    return '.'.join(parts[len(parts) - pivot - 2:])


def getViews():
    results = []
    for reg in templateViewRegistrations():
        if ITTWViewTemplate.providedBy(reg.factory):
            continue
        else:
            attr, pt = findViewletTemplate(reg.factory)
            if attr is None:  # skip, if the factory has no template...
                continue
            results.append(pt)
    return results


def getSkins(context):
    skins_tool = getToolByName(context, 'portal_skins')
    skin = skins_tool.getDefaultSkin()
    skin_path = skins_tool.getSkinPath(skin)
    if skin_path is None:
        return []

    results = []
    for layer_path in skin_path.split(','):
        try:
            layer_folder = skins_tool.unrestrictedTraverse(layer_path)
        except KeyError:
            # Sometimes the active theme declares nonexistent folders
            # this is not themeeditors fault, so we skip the error
            continue
        for name, obj in layer_folder.items():
            if isinstance(obj, FSObject):
                results.append(obj)
    return results


class ResourcesView(BrowserView):

    def __call__(self):
        self.jbot_path = 'jbot/%s' % self.context.getId()
        results = self.skins()
        results.extend(self.views())
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(results)

    def views(self):
        results = []
        for pt in getViews():
            filename = pt.filename
            if self.jbot_path in filename:
                zptfile = filename.split(self.jbot_path)[1]
            else:
                zptfile = mangleAbsoluteFilename(filename)
            results.append(zptfile)
        return results

    def skins(self):
        results = []
        for obj in getSkins(self.context):
            results.append(mangleAbsoluteFilename(obj._filepath))
        return results


class CustomizeView(BrowserView):

    def __call__(self):
        authenticator = getMultiAdapter((self.context, self.request),
                                        name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized

        resource = self.request.get('resource')

        persistent = getUtility(
            IResourceDirectory, name="persistent")[RESOURCE_DIRECTORY_NAME]
        directory = persistent['custom']

        if resource in directory:
            # ignore, already customized
            return

        # check views first
        found = None
        for pt in getViews():
            if resource == mangleAbsoluteFilename(pt.filename):
                found = pt.filename
                break
        if not found:
            for obj in getSkins(self.context):
                if resource == mangleAbsoluteFilename(obj._filepath):
                    found = obj._filepath
                    break
        if found:
            fi = open(found)
            persistent.writeFile('custom/' + resource, fi)
            fi.close()
