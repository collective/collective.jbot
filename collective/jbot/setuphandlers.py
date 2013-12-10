from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from interfaces import RESOURCE_DIRECTORY_NAME


def install(context):
    # install jbot resource directory
    persistentDirectory = getUtility(IResourceDirectory, name="persistent")
    if RESOURCE_DIRECTORY_NAME not in persistentDirectory:
        persistentDirectory.makeDirectory(RESOURCE_DIRECTORY_NAME)
        jbot = persistentDirectory[RESOURCE_DIRECTORY_NAME]
        jbot.makeDirectory('custom')
