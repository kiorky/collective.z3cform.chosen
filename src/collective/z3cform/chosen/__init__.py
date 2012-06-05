import logging
from zope.i18nmessageid import MessageFactory
MessageFactory = collectivez3cformchosenMessageFactory = MessageFactory('collective.z3cform.chosen') 
logger = logging.getLogger('collective.z3cform.chosen')
def initialize(context):
    """Initializer called when used as a Zope 2 product.""" 
