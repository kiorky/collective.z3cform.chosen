from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser
from zope import interface, schema
from plone.theme.interfaces import IDefaultPloneLayer

from collective.z3cform.chosen import MessageFactory as _

import z3c.form

class IMyPortalUser(IPropertiedUser):
    """ Marker interface implemented by users in my portal. """

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer and a plone skin marker.
    """

class ILayer(interface.Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """ 

class IChosenWidget(z3c.form.interfaces.ISelectWidget):
    """."""
    onselect = schema.TextLine(
        title=u'On Select',
        description=(u'The ``onselect`` event occurs when a user selects '
                     u'some text in a text field.'),
        required=False) 
    readonly = schema.Choice(
        title=u'Read-Only',
        description=(u'When set for a form control, this boolean attribute '
                     u'prohibits changes to the control.'),
        values=(None, 'readonly'),
        required=False) 



