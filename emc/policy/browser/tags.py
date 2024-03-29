# -*- coding: utf-8 -*-
from plone.app.content.browser.contents import ContentsBaseAction
from plone.app.content.interfaces import IStructureAction
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import get_top_site_from_url
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import implementer


@implementer(IStructureAction)
class TagsAction(object):

    template = ViewPageTemplateFile('templates/tags.pt')
    order = 6

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_options(self):
        site = get_top_site_from_url(self.context, self.request)
        base_url = site.absolute_url()
        base_vocabulary = '%s/@@getVocabulary?name=' % getSite().absolute_url()
        return {
            'tooltip': translate(_('Tags'), context=self.request),
            'id': 'tags',
            'icon': 'tags',
            'url': '%s{path}/@@pt-fc-tags' % base_url,
            'form': {
                'template': self.template(
#                     vocabulary_url='%splone.app.vocabularies.Keywords' % (
                    vocabulary_url='%scollective.gtags.ProjectKeywords' % (
                        base_vocabulary)
                )
            }
        }


class TagsActionView(ContentsBaseAction):
    required_obj_permission = 'Modify portal content'
    success_msg = _('Successfully updated tags on items')
    failure_msg = _('Failed to modify tags on items')

    def action(self, obj):
        tmp = self.request.form.get('toadd')
        if tmp:
            tmp = set(tmp.split(','))
            if len(tmp) >1:
                tl = []
                tl.append(tmp.pop())
                toadd = set(tl)
            else:
                toadd = tmp
        else:
            toadd = set([])
        toremove = self.request.get('toremove')
        if toremove:
            toremove = set(toremove.split(','))
        else:
            toremove = set([])
        tags = set(obj.Subject())
        tags = tags - toremove
        tags = tags | toadd
        obj.setSubject(list(tags))
        obj.reindexObject()
