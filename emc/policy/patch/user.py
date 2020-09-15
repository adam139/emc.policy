# -*- coding: utf-8 -*-
"""
ZODB based user manager with introspection and management interfaces.
"""
from AccessControl import AuthEncoding
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import manage_users as ManageUsers
from App.class_init import InitializeClass
from App.special_dtml import DTMLFile
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.interfaces.capabilities import IDeleteCapability
from Products.PlonePAS.interfaces.capabilities import IPasswordSetCapability
from Products.PlonePAS.interfaces.plugins import IUserIntrospection
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PluggableAuthService.plugins.ZODBUserManager \
    import ZODBUserManager as BasePlugin
from Products.PluggableAuthService.utils import createViewName
from zope.interface import implementer



    #add by adam
    # todo self cache function based userid and rolename
def isRole(self,rolename):
        """True iff current login user has rolename role"""
        mtool = getToolByName(self, 'portal_membership')
        current = mtool.getAuthenticatedMember()
        curroles = current.getRoles()
#         import pdb
#         pdb.set_trace()
        return bool(rolename in curroles)        
    # implement interfaces IDeleteCapability, IPasswordSetCapability

