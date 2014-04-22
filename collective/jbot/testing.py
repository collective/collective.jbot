from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig
from plone.testing import z2
from plone.app.theming.utils import (
    getAvailableThemes, applyTheme, createThemeFromTemplate,
    getCurrentTheme)
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone.resource.utils import queryResourceDirectory
import os
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from interfaces import RESOURCE_DIRECTORY_NAME

_dir = os.path.dirname(__file__)
TEST_FILES_DIR = os.path.join(_dir, 'tests/files')

from plone.app import layout
ORIGINAL_RESOURCE = os.path.join(layout.__path__[0], 'viewlets/footer.pt')
CUSTOMIZED_RESOURCE = 'plone.app.layout.viewlets.footer.pt'


class JBOT(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import collective.jbot
        import plone.app.theming

        xmlconfig.file('configure.zcml', plone.app.theming,
                       context=configurationContext)
        z2.installProduct(app, 'plone.app.theming')

        xmlconfig.file('configure.zcml', collective.jbot,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.app.theming:default')
        applyProfile(portal, 'collective.jbot:default')


JBOT_FIXTURE = JBOT()
JBOT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(JBOT_FIXTURE,), name="JBOT:Integration")
JBOT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(JBOT_FIXTURE,), name="JBOT:Functional")


def getTheme(name):
    themes = getAvailableThemes()
    for theme in themes:
        if theme.__name__ == name:
            return theme


def activateTheme():
    theme = getTheme('custom')

    if theme is None:
        createThemeFromTemplate('custom', '')
        theme = getTheme('custom')
        directory = queryResourceDirectory(THEME_RESOURCE_NAME, 'custom')
        try:
            directory['jbot']
        except:
            directory.makeDirectory('jbot')
            fi = open(os.path.join(TEST_FILES_DIR, 'footer2.pt'))
            directory.writeFile('jbot/' + CUSTOMIZED_RESOURCE, fi)
            fi.close()

    if getCurrentTheme() != 'custom':
        applyTheme(theme)


def deactivateTheme():
    applyTheme(None)


def applyCustomizations():
    persistent = getUtility(
        IResourceDirectory, name="persistent")[RESOURCE_DIRECTORY_NAME]
    fi = open(os.path.join(TEST_FILES_DIR, 'footer.pt'))
    persistent.writeFile('custom/' + CUSTOMIZED_RESOURCE, fi)
    fi.close()


def removeCustomizations():
    persistent = getUtility(
        IResourceDirectory, name="persistent")[RESOURCE_DIRECTORY_NAME]
    directory = persistent['custom']
    del directory[CUSTOMIZED_RESOURCE]
