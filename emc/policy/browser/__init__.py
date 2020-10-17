# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Acquisition import aq_inner
from plone.app.content.browser.file import TUS_ENABLED
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.content.interfaces import IStructureAction
from plone.app.content.utils import json_dumps
from plone.app.content.utils import json_loads
from plone.app.content.browser.contents import FolderContentsView
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.protect.postonly import check as checkpost
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone import utils
from Products.CMFPlone.interfaces.controlpanel import ISiteSchema
from Products.CMFPlone.utils import get_top_site_from_url
from Products.Five import BrowserView
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer

from emc.policy.interfaces import IProjectStructureAction

import six
import zope.deferredimport

def initialize(context):
    """Initializer called when used as a Zope 2 product."""


@implementer(IFolderContentsView)
class ProjectFolderContentsView(FolderContentsView):

    def get_actions(self):
        actions = []
        for name, Utility in getUtilitiesFor(IStructureAction):
            if name == "tags":continue
            utility = Utility(self.context, self.request)
            actions.append(utility)
        for name, Utility in getUtilitiesFor(IProjectStructureAction):
            utility = Utility(self.context, self.request)
            actions.append(utility)
        actions.sort(key=lambda a: a.order)
        return [a.get_options() for a in actions]
    
    def get_options(self):
        site = get_top_site_from_url(self.context, self.request)
        base_url = site.absolute_url()
        base_vocabulary = '%s/@@getVocabulary?name=' % base_url
        site_path = site.getPhysicalPath()
        context_path = self.context.getPhysicalPath()
        columns = self.get_columns()
        options = {
            'vocabularyUrl': '%splone.app.vocabularies.Catalog' % (
                base_vocabulary),
            'urlStructure': {
                'base': base_url,
                'appended': '/project_contents'
            },
            'moveUrl': '%s{path}/fc-itemOrder' % base_url,
            'indexOptionsUrl': '%s/@@qsOptions' % base_url,
            'contextInfoUrl': '%s{path}/@@fc-contextInfo' % base_url,
            'setDefaultPageUrl': '%s{path}/@@fc-setDefaultPage' % base_url,
            'availableColumns': columns,
            'attributes': ['Title', 'path', 'getURL', 'getIcon', 'getMimeIcon', 'portal_type'] + list(columns.keys()),  # noqa
            'buttons': self.get_actions(),
            'rearrange': {
                'properties': self.get_indexes(),
                'url': '%s{path}/@@fc-rearrange' % base_url
            },
            'basePath': '/' + '/'.join(context_path[len(site_path):]),
            'upload': {
                'relativePath': 'fileUpload',
                'baseUrl': base_url,
                'initialFolder': IUUID(self.context, None),
                'useTus': TUS_ENABLED
            },
            'thumb_scale': self.get_thumb_scale(),
        }
        return options
