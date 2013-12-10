from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.FSObject import FSObject
import json
from plone.app.customerize.registration import templateViewRegistrations
from five.customerize.utils import findViewletTemplate
from five.customerize.interfaces import ITTWViewTemplate


def mangleAbsoluteFilename(filename):
    parts = filename.split('/')
    pivot = 0
    for idx, part in enumerate(reversed(parts[:-2])):
        if '.' in part:
            pivot = idx
            break
    return '.'.join(parts[len(parts) - pivot - 2:])


class ResourcesView(BrowserView):

    def __call__(self):
        results = self.skins()
        results.extend(self.views())
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(results)

    def views(self):
        results = []
        for reg in templateViewRegistrations():
            if ITTWViewTemplate.providedBy(reg.factory):
                continue
            else:
                attr, pt = findViewletTemplate(reg.factory)
                if attr is None:  # skip, if the factory has no template...
                    continue
                zptfile = mangleAbsoluteFilename(pt.filename)
                results.append(zptfile)
        return results

    def skins(self):
        skins_tool = getToolByName(self.context, 'portal_skins')
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
                    results.append(mangleAbsoluteFilename(obj._filepath))
        return results
