from plone.resource.traversal import ResourceTraverser
from interfaces import RESOURCE_DIRECTORY_NAME


class JbotResourceTraverser(ResourceTraverser):
    name = RESOURCE_DIRECTORY_NAME
