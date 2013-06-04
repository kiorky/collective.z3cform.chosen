import os, sys

from setuptools import setup, find_packages

version = '1.2.dev0'

def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [read('README.rst'),
     read('src', 'collective', 'z3cform', 'chosen', 'README.txt'),
     read('docs', 'INSTALL.rst'),
     read('docs', 'CHANGES.rst'),
    ]
)

classifiers = [
    "Framework :: Plone",
    "Framework :: Plone :: 4.0",
    "Framework :: Plone :: 4.1",
    "Framework :: Plone :: 4.2",
    "Programming Language :: Python",
    "Topic :: Software Development",]

name = 'collective.z3cform.chosen'
setup(
    name=name,
    namespace_packages=[         'collective',         'collective.z3cform',
    ],
    version=version,
    description='chosen widget for z3cform (both chosen & ajax version)',
    long_description=long_description,
    classifiers=classifiers,
    keywords='chosen z3cform widget plone',
    author='kiorky',
    author_email='kiorky@cryptelium.net',
    url='http://pypi.python.org/pypi/%s' % name,
    license='GPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'z3c.autoinclude',
        'Plone',
        'demjson',
        'ordereddict',
        'plone.app.upgrade',
        # with_ploneproduct_jschosen
        'collective.js.chosen',
        'z3c.formwidget.query',
        # -*- Extra requirements: -*-
    ],
    extras_require = {
        'test': ['plone.app.testing',]
    },
    entry_points = {
        'z3c.autoinclude.plugin': ['target = plone',],
    },
)
# vim:set ft=python:
