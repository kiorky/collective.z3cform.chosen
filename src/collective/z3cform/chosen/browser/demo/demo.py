from plone.z3cform import layout
from Products.CMFCore.utils import getToolByName
from z3c.form import form, button, field
from z3c.formwidget.query.interfaces import IQuerySource
from zope.component import adapts
from zope.interface import Interface, implements
from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from ordereddict import OrderedDict

from collective.z3cform.chosen.widget import (
    AjaxChosenFieldWidget,
    AjaxChosenMultiFieldWidget,
    ChosenFieldWidget,
    ChosenMultiFieldWidget,
)

DATA = OrderedDict()
DATA["11"] ="aaa"
DATA["22"] ="bbb"
DATA["13"] ="ccc"
DATA["14"] ="ddd"
DATA["15"] ="eee"
DATA["17"] ="fff"
DATA["16"] ="faa"
DATA["18"] ="fbb"
DATA["29"] ="fcc"
DATA["20"]="fcd"

class KeywordSource(object):
    implements(IQuerySource)

    def __init__(self, context):
        self.context = context
        self.vocab = SimpleVocabulary(
            [SimpleVocabulary.createTerm(DATA[x], x, DATA[x])
             for x in DATA]
        )

    def __contains__(self, term):
        return self.vocab.__contains__(term)

    def __iter__(self):
        return self.vocab.__iter__()

    def __len__(self):
        return self.vocab.__len__()

    def getTerm(self, value):
        return self.vocab.getTerm(value)

    def getTermByToken(self, value):
        return self.vocab.getTermByToken(value)

    def search(self, query_string):
        q = query_string.lower()
        return [kw
                for kw in self.vocab._terms
                if q.lower() in kw.value]


class KeywordSourceBinder(object):
    implements(IContextSourceBinder)

    def __call__(self, context):
        return KeywordSource(context)


class ITestForm(Interface):

    single_keyword = schema.Choice(
        title=u"Single",
        source=KeywordSourceBinder(),
        required=False)

    keywords = schema.List(
        title=u"Multiple",
        value_type=schema.Choice(
            title=u"Multiple",
            source=KeywordSourceBinder()),
        required=False)

    asingle_keyword = schema.Choice(
        title=u"Ajax Single",
        source=KeywordSourceBinder(),
        required=False)

    akeywords = schema.List(
        title=u"Ajax Multiple",
        value_type=schema.Choice(
            title=u"Multiple",
            source=KeywordSourceBinder()),
        required=False)


class TestForm(form.Form):
    fields = field.Fields(ITestForm)
    fields['single_keyword'].widgetFactory = ChosenFieldWidget
    fields['keywords'].widgetFactory = ChosenMultiFieldWidget
    fields['asingle_keyword'].widgetFactory = AjaxChosenFieldWidget
    fields['akeywords'].widgetFactory = AjaxChosenMultiFieldWidget

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors


class ContextLessTestForm(TestForm):
    ignoreContext=True


class TestAdapter(object):
    implements(ITestForm)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def _get_single_keyword(self):
        return DATA["11"]

    def _set_single_keyword(self, value):
        print "setting", value

    single_keyword = property(_get_single_keyword, _set_single_keyword)

    def _get_keywords(self):
        return [DATA["11"]]

    def _set_keywords(self, value):
        print "setting", value

    keywords = property(_get_keywords, _set_keywords)

    def _get_single_akeyword(self):
        return DATA["11"]

    def _set_single_akeyword(self, value):
        print "setting", value

    asingle_keyword = property(_get_single_akeyword, _set_single_akeyword)

    def _get_akeywords(self):
        return [DATA["11"]]

    def _set_akeywords(self, value):
        print "setting", value

    akeywords = property(_get_akeywords, _set_akeywords)


TestView = layout.wrap_form(TestForm)
ContextLessTestView = layout.wrap_form(ContextLessTestForm)

