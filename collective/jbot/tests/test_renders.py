import unittest
from collective.jbot.testing import JBOT_FUNCTIONAL_TESTING
from collective.jbot.testing import (
    activateTheme, deactivateTheme, applyCustomizations,
    removeCustomizations, TEST_FILES_DIR, CUSTOMIZED_RESOURCE)
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login
from plone.testing.z2 import Browser
import transaction
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from collective.jbot.interfaces import RESOURCE_DIRECTORY_NAME
from StringIO import StringIO


class TestRender(unittest.TestCase):

    layer = JBOT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.portalUrl = self.portal.absolute_url()

    def test_render_customization(self):
        applyCustomizations()
        transaction.commit()
        self.browser.open(self.portalUrl)
        self.assertIn('<div>foobar</div>', self.browser.contents)
        removeCustomizations()
        transaction.commit()

    def test_render_theme_customization(self):
        applyCustomizations()
        activateTheme()
        transaction.commit()
        self.browser.open(self.portalUrl)
        self.assertIn('<div>foobar2</div>', self.browser.contents)
        removeCustomizations()
        deactivateTheme()
        transaction.commit()

    def test_remove_customization(self):
        applyCustomizations()
        transaction.commit()
        self.browser.open(self.portalUrl)
        self.assertIn('<div>foobar</div>', self.browser.contents)
        removeCustomizations()
        transaction.commit()
        self.browser.open(self.portalUrl)
        self.assertNotIn('<div>foobar</div>', self.browser.contents)

    def test_new_customization(self):
        applyCustomizations()
        transaction.commit()

        self.browser.open(self.portalUrl)
        self.assertIn('<div>foobar</div>', self.browser.contents)

        # customize again
        persistent = getUtility(
            IResourceDirectory, name="persistent")[RESOURCE_DIRECTORY_NAME]
        fi = StringIO()
        fi.write('<div>foobarcustom</div>')
        persistent.writeFile('custom/' + CUSTOMIZED_RESOURCE, fi)
        transaction.commit()

        self.browser.open(self.portalUrl)
        self.assertIn('<div>foobarcustom</div>', self.browser.contents)

        removeCustomizations()
        transaction.commit()
