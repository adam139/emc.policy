from plone import api
import logging

PROFILE_ID = 'profile-emc.policy:postinstall'


def disable_add2siteroot(context, logger=None):
    """Method to convert float Price fields to string.

    When called from the import_various method, 'context' is
    the plone site and 'logger' is the portal_setup logger.

    But this method will be used as upgrade step, in which case 'context'
    will be portal_setup and 'logger' will be None."""

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('emc.policy')

    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
    logger.info('import postinstall profile')