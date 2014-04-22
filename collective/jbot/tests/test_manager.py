import unittest
from collective.jbot.testing import (
    JBOT_INTEGRATION_TESTING, activateTheme, deactivateTheme,
    applyCustomizations, CUSTOMIZED_RESOURCE, ORIGINAL_RESOURCE,
    removeCustomizations)
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login
from zope.globalrequest import setRequest
from collective.jbot.manager import Storage, TemplateManager
from collective.jbot.interfaces import REQ_CACHE_KEY


class TestJBOT(unittest.TestCase):

    layer = JBOT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRequest(self.request)
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def tearDown(self):
        self.clearRequest()

    def clearRequest(self):
        for key in self.request.environ.keys():
            if key.startswith(REQ_CACHE_KEY):
                del self.request.environ[key]

    def test_get_storage(self):
        storage = Storage()
        self.assertTrue(storage.directory is not None)

    def test_get_storage_with_theme(self):
        storage = Storage()
        self.assertTrue(storage.themeDirectory is None)
        activateTheme()
        storage = Storage()
        self.assertTrue(storage.themeDirectory is not None)
        deactivateTheme()

    def test_contains(self):
        applyCustomizations()
        storage = Storage()
        self.assertTrue('plone.app.layout.viewlets.footer.pt' in storage)
        removeCustomizations()

    def test_contains_with_theme(self):
        activateTheme()
        storage = Storage()
        self.assertTrue('plone.app.layout.viewlets.footer.pt' in storage)
        deactivateTheme()

    def test_does_not_contain(self):
        storage = Storage()
        self.assertTrue('plone.app.layout.viewlets.footer.pt' not in storage)

    def test_get_file_with_no_customizations(self):
        class FakeTemplate(object):
            filename = ORIGINAL_RESOURCE

        template = FakeTemplate()
        mng = TemplateManager('manager')
        self.assertFalse(mng.registerTemplate(template, CUSTOMIZED_RESOURCE))
        self.assertFalse(hasattr(template, '_filename'))

    def test_get_file(self):
        applyCustomizations()

        class FakeTemplate(object):
            filename = ORIGINAL_RESOURCE

        template = FakeTemplate()
        mng = TemplateManager('manager')
        self.assertTrue(mng.registerTemplate(template, CUSTOMIZED_RESOURCE))
        self.assertEquals(template._filename, ORIGINAL_RESOURCE)
        self.assertTrue(template.filename.endswith(CUSTOMIZED_RESOURCE))

        removeCustomizations()

    def test_remove_file(self):
        applyCustomizations()

        class FakeTemplate(object):
            filename = ORIGINAL_RESOURCE

        template = FakeTemplate()

        mng = TemplateManager('manager')
        mng.registerTemplate(template, CUSTOMIZED_RESOURCE)

        removeCustomizations()
        self.clearRequest()

        mng = TemplateManager('manager')

        self.assertTrue(mng.registerTemplate(template, CUSTOMIZED_RESOURCE))
        self.assertEquals(template.filename, ORIGINAL_RESOURCE)
