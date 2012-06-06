import demjson
from ordereddict import OrderedDict

import zope.component
from zope.i18n import translate
from zope.interface import implementsOnly, implementer
from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.interfaces import ITitledTokenizedTerm

from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from Acquisition import Explicit
from Acquisition.interfaces import IAcquirer
from App.class_init import InitializeClass

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import z3c.form
from z3c.form.browser import select
from z3c.formwidget.query.widget import (QueryTerms, SourceTerms)

from collective.z3cform.chosen import MessageFactory as _
from collective.z3cform.chosen.interfaces import IChosenWidget
demjson.dumps = demjson.encode
demjson.loads = demjson.decode

def jsbool(value):
    if value:
        return 'true'
    else:
        return 'false'

class ChosenAutocompleteSearch(BrowserView):
    def validate_access(self):

        content = self.context.form.context

        # If the object is not wrapped in an acquisition chain
        # we cannot check any permission.
        if not IAcquirer.providedBy(content):
            return

        url = self.request.getURL()
        view_name = url[len(content.absolute_url()):].split('/')[1]

        # May raise Unauthorized

        # If the view is 'edit', then traversal prefers the view and
        # restrictedTraverse prefers the edit() method present on most CMF
        # content. Sigh...
        if not view_name.startswith('@@') and not view_name.startswith('++'):
            view_name = '@@' + view_name

        view_instance = content.restrictedTraverse(view_name)
        sm = getSecurityManager()
        sm.validate(content, content, view_name, view_instance)
    def __call__(self):

        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        self.validate_access()

        query = self.request.get('term', None)
        if not query:
            return ''

        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        self.context.update()
        source = self.context.bound_source

        if query:
            terms = set(source.search(query))
        else:
            terms = set()

        self.request.response.setHeader(
            'Content-Type', 'application/javascript')
        return demjson.dumps(
            [(t.token, t.title or t.value or t.token)
             for t in sorted(
                 terms,
                 key=lambda t: t.value or t.title)])


class ChosenBase(select.SelectWidget, Explicit):
    implementsOnly(IChosenWidget)
    security = ClassSecurityInfo()
    security.declareObjectPublic()

    _bound_source = None

    input_template = ViewPageTemplateFile('input.pt')
    display_template = ViewPageTemplateFile('display.pt')
    hidden_template = ViewPageTemplateFile('hidden.pt')

    # load values from bounded source at initialisation
    populate_select = False

    # Options passed to jQuery auto-completer
    onselect = ""
    readonly = False
    prompt = True
    promptMessage = _('select a value or '
                      'this for no value...')
    noValueMessage = _('no value')
    noValueToken = _(u'(nothing)')
    no_results_text = _("No results found")
    style = "width:280px;"
    multiple = False
    allow_single_deselect = False
    search_url = "%s/++widget++%s/@@chosen-autocomplete-search"

    # JavaScript template
    js_template = """\
    (function($) {
        $().ready(function() {
            $('#%(id)s-select').data('klass','%(klass)s').data('title','%(title)s');
            $('#%(id)s-select').chosen({
                allow_single_deselect: %(allow_single_deselect)s,
                no_results_text: '%(no_results_text)s'
            });
            %(js_extra)s
        });
    })(jQuery);
    """
    ajax_js_template = """\
    (function($) {
      $().ready(function() {
          $('#%(id)s-select').data('klass','%(klass)s').data('title','%(title)s');
          $('#%(id)s-select').ajaxChosen(
            {
                method: '%(method)s',
                url: '%(url)s',
                dataType: '%(datatype)s'
            },
            %(ajax_callback)s,
            null,
            {allow_single_deselect:%(allow_single_deselect)s,
             no_results_text: '%(no_results_text)s'}
          );
          %(js_extra)s
      });
    })(jQuery);
    """
    method = 'GET'
    datatype = 'json'
    ajax_callback = """\
    function (data) {
        var terms = {};
        $.each(data, function (i, val) {
            terms[val[0]] = val[1];
        });
        return terms;
    }"""

    @property
    def source(self):
        """We need to bind the field to the context so that vocabularies
        appear as sources"""
        return self.field.bind(self.context).source

    @property
    def placeholder(self):
        return self.promptMessage

    @property
    def bound_source(self):
        if self._bound_source is None:
            source = self.source
            if IContextSourceBinder.providedBy(source):
                source = source(self.context)
            assert ISource.providedBy(source)
            self._bound_source = source
        return self._bound_source

    @property
    def autocomplete_url(self):
        """Generate the URL that returns autocomplete results for this form
        """
        form_url = self.request.getURL()
        return self.search_url % (form_url, self.name)


    # Override this to insert additional JavaScript
    def js_extra(self):
        return ""

    def __call__(self):
        self.update()
        return self.render()

    def render(self):
        utemplate = None
        if self.mode == z3c.form.interfaces.DISPLAY_MODE:
            utemplate = self.display_template
        if self.mode == z3c.form.interfaces.INPUT_MODE:
            utemplate = self.input_template
        if self.mode == z3c.form.interfaces.HIDDEN_MODE:
            utemplate = self.hidden_template
        if bool(utemplate):
            return utemplate(self)

    def update(self):
        # Allow the source to provide terms until we have more specific ones
        # from the query.
        # Things do not go well if self.terms is None
        self._bound_source = None
        source = self.bound_source
        terms = OrderedDict()

        # populate select values if needed
        if self.populate_select:
            for t in self.source:
                if not t.token in terms:
                    terms[t.token] = t

        # pre defined terms from context+source
        self.terms = SourceTerms(self.context, self.request, self.form, self.field, self, source)

        # If we have values in the request,
        # use these to get the terms.
        request_values = z3c.form.interfaces.NOVALUE
        # extract selected value
        if not self.ignoreRequest:
            request_values = self.extract(
                default=z3c.form.interfaces.NOVALUE)

        if request_values is not z3c.form.interfaces.NOVALUE:
            if not isinstance(request_values, (tuple, set, list)):
                request_values = (request_values,)

            for token in request_values:
                if not token or token == self.noValueToken:
                    continue
                try:
                    t = source.getTermByToken(token)
                    terms[t.token] = t
                except LookupError:
                    # Term no longer available
                    if not self.ignoreMissing:
                        raise

        # take the value from the current saved value
        # if there is an existing adapter allowing it
        if not self.ignoreContext:
            selection = zope.component.getMultiAdapter(
                (self.context, self.field),
                z3c.form.interfaces.IDataManager).query()
            if selection is z3c.form.interfaces.NOVALUE:
                selection = []
            elif not isinstance(selection,
                                (tuple, set, list)):
                selection = [selection]
            for value in selection:
                if not value:
                    continue
                try:
                    t = source.getTerm(value)
                    terms[t.token] = t
                except LookupError:
                    # Term no longer available
                    if not self.ignoreMissing:
                        raise
        # re-set terms with values from request
        self.terms = QueryTerms(self.context, self.request, self.form, self.field, self, terms.values())

        # update widget selected value if any
        select.SelectWidget.update(self)

    def js(self):
        return self.js_template % dict(
            id=self.id,
            url=self.autocomplete_url,
            klass=self.klass,
            allow_single_deselect=jsbool( self.allow_single_deselect),
            title=self.title,
            method = self.method,
            datatype = self.datatype,
            ajax_callback = self.ajax_callback,
            no_results_text=self.no_results_text,
            js_extra=self.js_extra())

    @property
    def items(self):
        items = []
        if self.terms is not None:
            # update() has been called
            if ((not self.required or self.prompt)
                and not bool(self.multiple)):
                message = self.noValueMessage
                if self.prompt:
                    message = self.promptMessage
                items.append({
                    'id': self.id + '-novalue',
                    'value': self.noValueToken,
                    'content': message,
                    'selected': self.value == []
                    })
            for count, term in enumerate(self.terms):
                selected = self.isSelected(term)
                id = '%s-%i' % (self.id, count)
                content = term.token
                if ITitledTokenizedTerm.providedBy(term):
                    content = translate(
                        term.title,
                        context=self.request,
                        default=term.title)
                items.append(
                    {'id':id,
                     'value':term.token,
                     'content':content,
                     'selected':selected})
        return items


class MultiChosenBase(ChosenBase):
    """."""
    multiple = True
    @property
    def source(self):
        return self.field.bind(self.context).value_type.source


class AjaxChosenBase(ChosenBase):
    """."""


class MultiAjaxChosenBase(AjaxChosenBase,
                          MultiChosenBase):
    """."""
    multiple = True
    @property
    def source(self):
        return MultiChosenBase.source.fget(self)


InitializeClass(ChosenBase)
InitializeClass(AjaxChosenBase)


class ChosenSelectionWidget(ChosenBase):
    """widget that allows single selection.
    """
    klass = u'chosen-selection-widget'
    populate_select = True


class ChosenMultiSelectionWidget(MultiChosenBase):
    """widget that allows multiple selection
    """
    populate_select = True
    klass = u'chosen-multiselection-widget'


class AjaxChosenSelectionWidget(AjaxChosenBase):
    """Autocomplete widget that allows single selection.
    """
    klass = u'ajaxchosen-selection-widget'
    js_template = ChosenBase.ajax_js_template


class AjaxChosenMultiSelectionWidget(MultiAjaxChosenBase):
    """Autocomplete widget that allows multiple selection
    """
    klass = u'ajaxchosen-multiselection-widget'
    js_template = ChosenBase.ajax_js_template


@implementer(z3c.form.interfaces.IFieldWidget)
def ChosenFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        ChosenSelectionWidget(request))


@implementer(z3c.form.interfaces.IFieldWidget)
def ChosenMultiFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        ChosenMultiSelectionWidget(request))


@implementer(z3c.form.interfaces.IFieldWidget)
def AjaxChosenFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        AjaxChosenSelectionWidget(request))


@implementer(z3c.form.interfaces.IFieldWidget)
def AjaxChosenMultiFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        AjaxChosenMultiSelectionWidget(request))

