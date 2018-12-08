# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.lifecycleevent import ObjectModifiedEvent
from plone import api
from plone.app.dexterity.behaviors import constrains
from logging import getLogger
from zope import event
from emc.memberArea.events import MemberAreaCreatedEvent
from emc.project.behaviors.localroles import Ilocalroles
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from emc.policy.migration import add_navigator_portlet

logger = getLogger(__name__)


STRUCTURE = [
    {
        'type': 'emc.project.projectFolder',
        'title': u'项目管理',
        'id': 'project_folder',
        'description': u'项目容器',
        'layout': 'ajax_listings',
        'children': [
                     {
            'type': 'emc.project.project',
            'title': u'笔记本E210',
            'id': 'notebooke210',
            'description': u'笔记本E210EMC项目',
            'layout': 'ajax_listings',
            'children': [
                         {'type': 'emc.project.team',
                          'title': u'主板',
                          'id': 'motherboard',
                          'description': u'主板组',
                          
                          
                          'layout': 'ajax_listings',                          
                                             } ,  
                         {'type': 'emc.project.team',
                          'title': u'显卡',
                          'id': 'displaycard',
                          'description': u'显卡',
                          
                          
                          'layout': 'ajax_listings',
                           'children': [
                                        {'type': 'emc.project.doc',
                                         'title': u'显卡分析',
                                         'id': 'analysis',
                                         'description': u'显卡分析文档',
                                         
                                                                   
                                                                             } ,  
                                        {'type': 'emc.project.doc',
                                         'title': u'显卡设计',
                                         'id': 'design',
                                         'description': u'显卡设计文档',
                                         
                                         
                                                                         } ,    
                                        {'type': 'emc.project.doc',
                                         'title': u'显卡审核',
                                         'id': 'audit',
                                         'description': u'显卡审核文档',
                                         
                                         
                                                                         } ,  
                                        {'type': 'emc.project.doc',
                                         'title': u'故障诊断',
                                         'id': 'diagnose',
                                         'description': u'故障诊断文档',
                                         
                                         
                                                                         } ,                                                                                       
                         
                                                                        ]
                                             } ,                                                
                         {'type': 'emc.project.team',
                          'title': u'网卡',
                          'id': 'network',
                          'description': u'网卡',
                          
                          
                          'layout': 'ajax_listings',
                           'children': [
                                        {'type': 'emc.project.doc',
                                         'title': u'网卡分析',
                                         'id': 'analysis',
                                         'description': u'网卡分析文档',
                                         
                                                                   
                                                                             } ,  
                                        {'type': 'emc.project.doc',
                                         'title': u'网卡设计',
                                         'id': 'design',
                                         'description': u'网卡设计文档',
                                         
                                         
                                                                         } ,    
                                        {'type': 'emc.project.doc',
                                         'title': u'网卡审核',
                                         'id': 'audit',
                                         'description': u'网卡审核文档',
                                         
                                         
                                                                         } ,  
                                        {'type': 'emc.project.doc',
                                         'title': u'故障诊断',
                                         'id': 'diagnose',
                                         'description': u'故障诊断文档',
                                         
                                         
                                                                         } ,                                                                                       
                         
                                                                        ]
                                             } ,                            
                                            ]
                      },
           
                ]
    },
{
        'type': 'emc.kb.folder',
        'title': u'知识库',
        'id': 'kb_folder',
        'description': u'知识库',
        'layout': 'folder_contents',
        'children': [{
                      'type': 'emc.kb.ormfolder',
                      'title': u'数据库',
                      'id': 'ormfolder',
                      'description': u'问题库',
                      'layout': 'folder_contents',
                      },
                     {
                      'type': 'emc.kb.kbfolder',
                      'title': u'资源库',
                      'id': 'resources_folder',
                      'description': u'存放各种类型文件的容器',
                      'layout': 'folder_contents',
                                           
                      }]
        }               
]


def isNotCurrentProfile(context):
    return context.readDataFile('emcpolicy_marker.txt') is None

def setupGroups(context):
    """create emc management groups and management users
    """
    from emc.memberArea.events import BackMemberCreatedEvent
    group = api.group.create(
            groupname='System Administrators',
            title='System Administrators',
            description='EMC System Administrators',
            roles=['SysAdmin',],
            ) 
    group = api.group.create(
            groupname='Secure Staffs',
            title='Secure Staffs',
            description='EMC Secure Staffs',
            roles=['SecStaff', ],
            ) 
    group = api.group.create(
            groupname='Secure Auditors',
            title='Secure Auditors',
            description='EMC Secure Auditors',
            roles=['SecAuditor', ],
            )
    properties= dict(fullname=u'李四'.encode('utf-8'))
    demo = api.user.create(
            username='333010199106113321' ,
            email='lisi@plone.org',
            password='secret$',
            properties=properties
                               )
    if demo != None:
        event.notify(BackMemberCreatedEvent(demo))    
    properties= dict(fullname=u'系统管理员'.encode('utf-8'))
    demo = api.user.create(
            username='111111222222333333' ,
            email='sysadmin@plone.org',
            password='secret$',
            properties=properties
                               )
    if demo != None:
        event.notify(BackMemberCreatedEvent(demo))
    properties= dict(fullname=u'安全管理员'.encode('utf-8'))
    demo = api.user.create(
            username='444444555555666666' ,
            email='secstaff@plone.org',
            password='secret$',
            properties=properties
                               )
    if demo != None:
        event.notify(BackMemberCreatedEvent(demo))
    properties= dict(fullname=u'安全审计员'.encode('utf-8'))
    demo = api.user.create(
            username='777777888888999999' ,
            email='secauditor@plone.org',
            password='secret$',
            properties=properties
                               )
    if demo != None:
        event.notify(BackMemberCreatedEvent(demo))                    
    api.group.add_user(groupname='System Administrators', username='111111222222333333')
    api.group.add_user(groupname='Secure Staffs', username='444444555555666666')
    api.group.add_user(groupname='Secure Auditors', username='777777888888999999')


# def run_after(context):
def post_install(context):
    """post Setuphandler for the profile 'default'
    """
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package
#     return
    portal = api.portal.get()
    defaulpage = portal.get('front-page', None)
    if defaulpage is not None:
        api.content.delete(defaulpage)    
    members = portal.get('events', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('news', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('Members', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
       # give admin create memberarea
    pm = api.portal.get_tool(name='portal_membership')
    current = api.user.get_current()
    try:
        pm.memberareaCreationFlag = True
        pm.createMemberarea(member_id= current.id)      
        event.notify(MemberAreaCreatedEvent(current))
    except:
        return   
    for item in STRUCTURE:
        _create_content(item, portal) 
#     for i in range(1,20): 
# 
#         user = api.user.create(
#                                username='test%s' % i,
# #                                fullname=u'张测%s',
#                                email='test%s@plone.org' % i,
#                                password='secret',                               
#                                )
    setupGroups(context)    
    # add localroles 'Manager' to projectFolder for SecStuff
    
    try:
        portal['project_folder'].manage_setLocalRoles('444444555555666666',['Site Administrator'])
        portal['project_folder']['notebooke210'].manage_setLocalRoles('444444555555666666',['Site Administrator'])
    except:
        pass
    try:
        add_navigator_portlet(context)
    except:
        pass
                                                                
def _create_content(item, container):
    new = container.get(item['id'], None)
    if not new:
        new = api.content.create(
            type=item['type'],
            container=container,
            title=item['title'],
            description=item['description'],            
            id=item['id'],
            safe_id=False)
        logger.info('Created item {}'.format(new.absolute_url()))
    if item.get('layout', False):
        new.setLayout(item['layout'])
    if item.get('default-page', False):
        new.setDefaultPage(item['default-page'])
    if item.get('allowed_types', False):
        _constrain(new, item['allowed_types'])
    if item.get('local_roles', False):
        for local_role in item['local_roles']:
            api.group.grant_roles(
                groupname=local_role['group'],
                roles=local_role['roles'],
                obj=new)
    if item.get('publish', False):
        api.content.transition(new, to_state=item.get('state', 'published'))
    new.reindexObject()
    # call recursively for children
    for subitem in item.get('children', []):
        _create_content(subitem, new)


def _constrain(context, allowed_types):
    behavior = ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)
