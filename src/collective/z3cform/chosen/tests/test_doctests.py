"""
Launching all doctests in the tests directory using:

    - the base layer in testing.py

"""

from collective.z3cform.chosen.tests.base import FunctionalTestCase

################################################################################
# GLOBALS avalaible in doctests
# IMPORT/DEFINE objects there or inside ./user_globals.py (better)
# globals from the testing product are also available.
################################################################################
# example:
# from for import bar
# and in your doctests, you can do:
# >>> bar.something
from collective.z3cform.chosen.tests.globals import *
from collective.z3cform.chosen.testing import COLLECTIVE_Z3CFORM_CHOSEN_FUNCTIONAL_TESTING as FUNCTIONAL_TESTING
################################################################################


import unittest2 as unittest
import glob
import os
import logging
import doctest
from plone.testing import layered

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """."""
    logger = logging.getLogger('collective.z3cform.chosen.tests')
    cwd = os.path.dirname(__file__)
    pcwd = os.path.dirname(
        os.path.dirname(__file__)
    )
    files = []
    try:
        files = glob.glob(os.path.join(cwd, '*txt'))
        files.extend(glob.glob(os.path.join(pcwd, '*txt')))
        files = [f for f in files if not 'version.txt' in f]
    except Exception,e:
        logger.warn('No doctests for collective.z3cform.chosen')
    suite = unittest.TestSuite()
    globs = globals()
    for s in files:
        suite.addTests([
            layered(
                doctest.DocFileSuite(
                    s, 
                    globs = globs,
                    module_relative=False,
                    optionflags=optionflags,         
                ),
                layer=FUNCTIONAL_TESTING
            ),
        ])
    return suite
    


# vim:set ft=python:
