# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition.interfaces import IAcquirer
from Products.statusmessages.interfaces import IStatusMessage
from plone.dexterity.browser.base import DexterityExtensibleForm
from plone.dexterity.events import AddBegunEvent
from plone.dexterity.events import AddCancelledEvent
from plone.dexterity.i18n import MessageFactory as _
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.utils import getAdditionalSchemata
from plone.z3cform import layout
from plone.z3cform.interfaces import IDeferSecurityCheck
from z3c.form import button
from z3c.form import form
from zope.component import createObject
from zope.component import getUtility
from zope.event import notify
from zope.publisher.browser import BrowserPage
from collective.filepreviewbehavior.events import PreviewableFileCreatedEvent



def add(self, object):

        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        new_object = addContentToContainer(container, object)
#         import pdb
#         pdb.set_trace()
        notify(PreviewableFileCreatedEvent(new_object))

        if fti.immediate_view:
            self.immediate_view = "/".join(
                [container.absolute_url(), new_object.id, fti.immediate_view]
            )
        else:
            self.immediate_view = "/".join(
                [container.absolute_url(), new_object.id]
            )

