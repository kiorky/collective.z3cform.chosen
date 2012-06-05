import logging
import transaction
from Products.CMFCore.utils import getToolByName

from collective.z3cform.chosen import app_config
from collective.z3cform.chosen.app_config import PRODUCT_DEPENDENCIES, EXTENSION_PROFILES


def setupVarious(context):
    """Miscellanous steps import handle.
    """
    logger = logging.getLogger('collective.z3cform.chosen / setuphandler')

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.z3cform.chosen_various.txt') is None:
        return

    portal = context.getSite()

def setupQi(context):
    """Miscellanous steps import handle.
    """
    logger = logging.getLogger('collective.z3cform.chosen / setuphandler')

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.z3cform.chosen_qi.txt') is None:
        return

    portal = context.getSite() 
    portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    portal_setup = getToolByName(portal, 'portal_setup')
    logger = logging.getLogger('collective.z3cform.chosen.Install')

    for product in PRODUCT_DEPENDENCIES:
        logger.info('(RE)Installing %s.' % product)
        if not portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.installProduct(product)
            transaction.savepoint()

