#-*- coding: utf-8 -*-
"""Specific project configuration."""
GLOBALS = globals()




################################################################################
# Products that have entries in quickinstaller,
# here are their 'id' (not the translated name)
################################################################################

PRODUCT_DEPENDENCIES = (\
)

EXTENSION_PROFILES = ('collective.z3cform.chosen:default',)

SKIN = 'collective.z3cform.skin'
HIDDEN_PRODUCTS = [u'plone.app.openid', u'NuPlone',
#      u'collective.js.chosen',
#    u'collective.z3cform.chosen.migrations.v1_1',
#    u'collective.z3cform.chosen.migrations',
]
HIDDEN_PROFILES = [u'plone.app.openid', u'NuPlone',
    u'collective.z3cform.chosen.migrations.v11',
    u'collective.z3cform.chosen.migrations',
      u'collective.js.chosen',

]

from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts
from Products.CMFPlone.interfaces import INonInstallable as INonInstallableProfiles

class HiddenProducts(object):
    implements(INonInstallableProducts)

    def getNonInstallableProducts(self):
        return HIDDEN_PRODUCTS

class HiddenProfiles(object):
    implements(INonInstallableProfiles)

    def getNonInstallableProfiles(self):
        return [ u'plone.app.openid', u'NuPlone', ]
