#-*- coding: UTF-8 -*-
from zope.i18nmessageid import MessageFactory
import logging

_ = MessageFactory('emc.policy')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


import datetime
fmt = "%Y-%m-%d %H:%M:%S"

def list2str(lst):
    "transfer a list to string"
    initstr = ""
    for i in lst:
        if len(initstr) == 0 :initstr ="%s" % str(i)        
        else:
            initstr = "%s,%s" %(initstr,str(i))
    return initstr
        
def getfullname_orid(userobj):
    "if fullname exist then return fullname, else return id"
    fn=userobj.getProperty("fullname","")
    if bool(fn):
        return fn
    else:
        return userobj.getId()

    
def get_ip(request = None):
    """ Extract the client IP address from the HTTP request in a proxy-compatible way.

    @return: IP address as a string or None if not available
    """
    if request == None:
        from zope.globalrequest import getRequest
        request = getRequest()
    if request == None:return ""
    ip = request.get("HTTP_CLIENTIP",'')
    if bool(ip):
        logging.info("client ip:%s" % str(ip))        
        return ip    
    elif "HTTP_X_FORWARDED_FOR" in request.environ:
        # Virtual host
        ip = request.environ["HTTP_X_FORWARDED_FOR"]
    elif "HTTP_HOST" in request.environ:
        # Non-virtualhost
        ip = request.environ["REMOTE_ADDR"]
    else:
        # Unit test code?
        ip = ""

    return ip

       