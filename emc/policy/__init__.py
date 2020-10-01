#-*- coding: UTF-8 -*-
from zope.i18nmessageid import MessageFactory

import logging
logger = logging.getLogger(__name__)
import datetime
fmt = "%Y-%m-%d %H:%M:%S"
_ = MessageFactory('emc.policy')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

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
#         logger.info("fetched from HTTP_CLIENTIP,ip:%s,type:%s" % (ip,type(ip)))
        return ip    

    elif "HTTP_X_FORWARDED_FOR" in request.environ:
        # Virtual host
        ip = request.environ["HTTP_X_FORWARDED_FOR"]
        if len(ip.split(',')) > 1:
            ip = ip.split(',')[0]
#         logger.info("fetched from HTTP_X_FORWARDED_FOR,ip:%s,type:%s" % (ip,type(ip)))
        #fetched from HTTP_X_FORWARDED_FOR,ip:175.1.109.33, 172.23.0.7,type:<type 'str'>
        
    elif "HTTP_HOST" in request.environ:
        # Non-virtualhost
        ip = request.environ["REMOTE_ADDR"]
#         logger.info("fetched from REMOTE_ADDR,ip:%s,type:%s" % (ip,type(ip)))
    else:
        # Unit test code?
        ip = ""
    return ip
