from Testing import ZopeTestCase as ztc
import transaction
from OFS.Folder import Folder

import unittest2 as unittest

from zope.configuration import xmlconfig

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting as BIntegrationTesting, FunctionalTesting as BFunctionalTesting
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing.selenium_layers import SELENIUM_FUNCTIONAL_TESTING as SELENIUM_TESTING
from plone.testing import zodb, zca, z2

TESTED_PRODUCTS = (\
)

from plone.app.testing import (
    TEST_USER_ROLES,
    TEST_USER_NAME,
    TEST_USER_ID,
    SITE_OWNER_NAME,
)
from plone.app.testing.helpers import (
    login,
    logout,
)

PLONE_MANAGER_NAME = 'Plone_manager'
PLONE_MANAGER_ID = 'plonemanager'
PLONE_MANAGER_PASSWORD = 'plonemanager'

def print_contents(browser, dest='~/.browser.html'):
    """Print the browser contents somewhere for you to see its context
    in doctest pdb, type print_contents(browser) and that's it, open firefox
    with file://~/browser.html."""
    import os
    open(os.path.expanduser(dest), 'w').write(browser.contents)

class Browser(z2.Browser):
    def print_contents(browser, dest='~/.browser.html'):
        return print_contents(browser, dest)

class CollectiveZ3cformChosenLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )
    """Layer to setup the chosen site"""
    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def setUpZope(self, app, configurationContext):
        """Set up the additional products required for the collective.z3cform) site chosen.
        until the setup of the Plone site testing layer.
        """
        self.app = app
        self.browser = Browser(app)
        # old zope2 style products
        for product in TESTED_PRODUCTS:
            z2.installProduct(product)

        # ----------------------------------------------------------------------
        # Import all our python modules required by our packages
        # ---------------------------------------------------------------------
        #with_ploneproduct_jschosen
        import collective.js.chosen
        self.loadZCML('configure.zcml', package=collective.js.chosen)

        # -----------------------------------------------------------------------
        # Load our own chosen
        # -----------------------------------------------------------------------
        import collective.z3cform.chosen
        self.loadZCML('configure.zcml', package=collective.z3cform.chosen)

        # ------------------------------------------------------------------------
        # - Load the python packages that are registered as Zope2 Products
        #   which can't happen until we have loaded the package ZCML.
        # ------------------------------------------------------------------------

        #with_ploneproduct_jschosen
        z2.installProduct(app, 'collective.js.chosen')
        z2.installProduct(app, 'collective.z3cform.chosen')

        # -------------------------------------------------------------------------
        # support for sessions without invalidreferences if using zeo temp storage
        # -------------------------------------------------------------------------
        app.REQUEST['SESSION'] = self.Session()
        if not hasattr(app, 'temp_folder'):
            tf = Folder('temp_folder')
            app._setObject('temp_folder', tf)
            transaction.commit()
        ztc.utils.setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        self.portal = portal
        applyProfile(portal, 'collective.z3cform.chosen:default')


class LayerMixin(object):
    defaultBases = (CollectiveZ3cformChosenLayer() ,)

    def testSetUp(self):
        self.add_user(
            self['portal'],
            PLONE_MANAGER_ID,
            PLONE_MANAGER_NAME,
            PLONE_MANAGER_PASSWORD,
            ['Menager']+TEST_USER_ROLES)

    def add_user(self, portal, id, username, password, roles=None):
        if not roles: roles = TEST_USER_ROLES[:]
        self.loginAsPortalOwner()
        pas = portal['acl_users']
        pas.source_users.addUser(id, username, password)
        setRoles(portal, id, roles)
        self.logout()

    def loginAsPortalOwner(self):
        z2.login(self['app']['acl_users'], SITE_OWNER_NAME)

    def logout(self):
        logout()

class IntegrationTesting(LayerMixin, BIntegrationTesting):
    def testSetUp(self):
        BIntegrationTesting.testSetUp(self)
        LayerMixin.testSetUp(self)

class FunctionalTesting(LayerMixin, BFunctionalTesting):
    def testSetUp(self):
        BFunctionalTesting.testSetUp(self)
        LayerMixin.testSetUp(self) 

COLLECTIVE_Z3CFORM_CHOSEN_FIXTURE             = CollectiveZ3cformChosenLayer()
COLLECTIVE_Z3CFORM_CHOSEN_INTEGRATION_TESTING = IntegrationTesting(name = "CollectiveZ3cformChosen:Integration")
COLLECTIVE_Z3CFORM_CHOSEN_FUNCTIONAL_TESTING  = FunctionalTesting( name = "CollectiveZ3cformChosen:Functional")
COLLECTIVE_Z3CFORM_CHOSEN_SELENIUM_TESTING    = FunctionalTesting(bases = (SELENIUM_TESTING, COLLECTIVE_Z3CFORM_CHOSEN_FUNCTIONAL_TESTING,), name = "CollectiveZ3cformChosen:Selenium")

# vim:set ft=python:
