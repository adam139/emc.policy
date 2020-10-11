# -*- coding: utf-8 -*-
from BTrees.IIBTree import intersection
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone.app.vocabularies.terms import safe_encode
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import provider
from zope.interface import implementer
from emc.project.content.projectfolder import IProjectFolder
from Products.CMFPlone import PloneMessageFactory as _
from zope.site.hooks import getSite


"""
非密  60
内部  65
一般  70
重要  80
核心  90
空值 100
"""

# items = [ ('low', _('secret')),
#           ('mid', _('more secret')),
#           ('height', _('most secret'))          
#           ]
items = [ ('60', _('no secret')),
          ('65', _('inner')),
          ('70', _('normal secret')), 
          ('80', _('more secret')),
          ('90', _('most secret')),
          ('100', _('Null')),
          ]
terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
Vocabulary = SimpleVocabulary(terms)

@provider(IVocabularyFactory)
def safe_level_factory(context):
    return Vocabulary


@implementer(IVocabularyFactory)
class ExcludeProjectKeywordsVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the 'Subject' index

        >>> from plone.app.vocabularies.tests.base import DummyCatalog
        >>> from plone.app.vocabularies.tests.base import create_context
        >>> from plone.app.vocabularies.tests.base import DummyContent
        >>> from plone.app.vocabularies.tests.base import Request
        >>> from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex  # noqa

        >>> context = create_context()

        First test bytes vocabularies
        >>> rids = ('/1234', '/2345', '/dummy/1234')
        >>> tool = DummyCatalog(rids)
        >>> context.portal_catalog = tool
        >>> index = KeywordIndex('Subject')
        >>> done = index._index_object(
        ...     1,
        ...     DummyContent('ob1', [b'foo', b'bar', b'baz']), attr='Subject'
        ... )
        >>> done = index._index_object(
        ...     2,
        ...     DummyContent(
        ...         'ob2',
        ...         [b'blee', b'bar', u'non-åscii'.encode('utf8')]),
        ...         attr='Subject',
        ... )
        >>> tool.indexes['Subject'] = index
        >>> vocab = ExcludeProjectKeywordsVocabulary()
        >>> result = vocab(context)

        Value type is kept ...
        >>> expected = [b'bar', b'baz', b'blee', b'foo', u'non-åscii'.encode('utf8')]
        >>> sorted(result.by_value) == expected
        True

        ... but tokens are bytes on Python 2 and text in Python 3
        >>> if six.PY2:
        ...     expected = [b'bar', b'baz', b'blee', b'foo', b'non-=C3=83=C2=A5scii']
        ... else:
        ...     expected = [u'bar', u'baz', u'blee', u'foo', u'non-=C3=A5scii']
        >>> sorted(result.by_token) == expected
        True

        >>> result.getTermByToken(expected[-1]).title == u'non-åscii'
        True

        Testing unicode vocabularies
        First clear the index. Comparing non-six.text_type to six.text_type objects fails.
        >>> index.clear()
        >>> done = index._index_object(
        ...     1,
        ...     DummyContent('obj1', [u'äüö', u'nix']), attr='Subject'
        ... )
        >>> tool.indexes['Subject'] = index
        >>> vocab = ExcludeProjectKeywordsVocabulary()
        >>> result = vocab(context)
        >>> if six.PY2:
        ...     expected = [b'=C3=83=C2=A4=C3=83=C2=BC=C3=83=C2=B6', b'nix']
        ... else:
        ...     expected = [u'=C3=A4=C3=BC=C3=B6', u'nix']
        >>> sorted(result.by_token) == expected
        True
        >>> set(result.by_value) == {u'nix', u'äüö'}
        True
        >>> result.getTermByToken(expected[0]).title == u'äüö'
        True

    """
    # Allow users to customize the index to easily create
    # KeywordVocabularies for other keyword indexes
    keyword_index = 'Subject'
    path_index = 'path'

    def section(self, context):
        """gets section from which subjects are used.
        """
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        pjt = self.catalog(object_provides=IProjectFolder.__identifier__)
        if pjt:
            return pjt[0].getObject()
        else:
            return None

    def all_keywords(self, kwfilter):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex(self.keyword_index)
        return safe_simplevocabulary_from_values(index._index, query=kwfilter)

    def keywords_of_section(self, section, kwfilter):
        """Valid keywords under the given section.
        """
        pcat = getToolByName(section, 'portal_catalog')
        cat = pcat._catalog
        path_idx = cat.indexes[self.path_index]
        tags_idx = cat.indexes[self.keyword_index]
        result = []
        # query all oids of path - low level
        pquery = {
            self.path_index: {
                'query': '/'.join(section.getPhysicalPath()),
                'depth': -1,
            }
        }
        kwfilter = safe_encode(kwfilter)
        # uses internal zcatalog specific details to quickly get the values.
        path_result, info = path_idx._apply_index(pquery)
        for tag in tags_idx.uniqueValues():
            if kwfilter and kwfilter not in safe_encode(tag):
                continue
            tquery = {self.keyword_index: tag}
            tags_result, info = tags_idx._apply_index(tquery)
            if intersection(path_result, tags_result):
                result.append(tag)
        # result should be sorted, because uniqueValues are.
        return safe_simplevocabulary_from_values(result)

    def __call__(self, context, query=None):
        section = self.section(context)
        import pdb
        pdb.set_trace()
        if section is None:
            return self.all_keywords(query)
        #[item for item in x if item not in y]
        return [item for  item in self.all_keywords(query)  if item not in self.keywords_of_section(section, query)]


ExcludeProjectKeywordsVocabularyFactory = ExcludeProjectKeywordsVocabulary()
