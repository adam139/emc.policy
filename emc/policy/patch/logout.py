from AccessControl.SecurityManagement import getSecurityManager
from zope import event
import datetime
from emc.policy.events import AddlogoutEvent,NormalUserlogoutEvent
from emc.policy import get_ip,fmt,list2str,getfullname_orid

def logout(self, REQUEST):
    """Publicly accessible method to log out a user
    """
    user = getSecurityManager().getUser()

    logoutEvent = NormalUserlogoutEvent(userid = getfullname_orid(user),
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = get_ip(),
                                     type = 0,
                                     description = "",
                                     result = 1)

    if logoutEvent.available():
        if logoutEvent.is_normal_user():
            event.notify(logoutEvent)
        else:
            logoutEvent = AddlogoutEvent(adminid = getfullname_orid(user),
                                     userid = " ",
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = get_ip(),
                                     type = 0,
                                     description = "",
                                     result = 1)
            event.notify(logoutEvent)
            
                    
    self.resetCredentials(REQUEST, REQUEST['RESPONSE'])

    # Little bit of a hack: Issuing a redirect to the same place
    # where the user was so that in the second request the now-destroyed
    # credentials can be acted upon to e.g. go back to the login page
    referrer = REQUEST.get('HTTP_REFERER') # optional header
    #referrer = "192.168.0.5/v4/public/index.php?action=logout"
    if referrer:
        REQUEST['RESPONSE'].redirect(referrer)