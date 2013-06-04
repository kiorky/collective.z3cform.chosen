Chosen widget
===================

collective.chosen.widget provides an autocomplete widget based on the
jQuery Autocomplete widget.

    >>> from collective.z3cform.chosen import AjaxChosenFieldWidget
    >>> from collective.z3cform.chosen import AjaxChosenMultiFieldWidget
    >>> from collective.z3cform.chosen import ChosenFieldWidget
    >>> from collective.z3cform.chosen import ChosenMultiFieldWidget

First, we need a vocabulary to search. This is shamelessly stolen from
z3c.formwidget.query, which we extend.


    >>> from zope.interface import implements
    >>> from z3c.formwidget.query.interfaces import IQuerySource
    >>> from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

    >>> class ItalianCities(object):
    ...     implements(IQuerySource)
    ...
    ...     vocabulary = SimpleVocabulary((
    ...         SimpleTerm(u'bologna',  'bologna', u'Bologna'),
    ...         SimpleTerm(u'palermo',  'palermo', u'Palermo'),
    ...         SimpleTerm(u'sorrento', 'sorrento', u'Sorrento'),
    ...         SimpleTerm(u'torino', 'torino', u'Torino')))
    ...
    ...     def __init__(self, context):
    ...         self.context = context
    ...
    ...     __contains__ = vocabulary.__contains__
    ...     __iter__ = vocabulary.__iter__
    ...     getTerm = vocabulary.getTerm
    ...     getTermByToken = vocabulary.getTermByToken
    ...
    ...     def search(self, query_string):
    ...         return [v
    ...                 for v in self
    ...          if query_string.lower() in v.value.lower()]

    >>> from zope.schema.interfaces import IContextSourceBinder

    >>> class ItalianCitiesSourceBinder(object):
    ...     implements(IContextSourceBinder)
    ...
    ...     def __call__(self, context):
    ...         return ItalianCities(context)

Then, we will set up a simple test form and context.

    >>> from zope.interface import alsoProvides
    >>> from OFS.SimpleItem import SimpleItem
    >>> from Testing.makerequest import makerequest
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> from z3c.form.interfaces import IFormLayer

    >>> def make_request(path, form={}):
    ...     app = SimpleItem('')
    ...     request = makerequest(app).REQUEST
    ...     request.form.update(form)
    ...     alsoProvides(request, IFormLayer)
    ...     alsoProvides(request, IAttributeAnnotatable)
    ...     request._script = path.split('/')
    ...     request._steps = []
    ...     request._resetURLS()
    ...     return request

    >>> from zope.interface import Interface
    >>> from zope import schema
    >>> from z3c.form import form, field, button
    >>> from plone.z3cform.layout import wrap_form

    >>> class ICities(Interface):
    ...     afavourite_city = schema.Choice(title=u"Favourite city",
    ...                                    source=ItalianCitiesSourceBinder(), required=False)
    ...     avisited_cities = schema.List(title=u"Visited cities",
    ...                                  value_type=schema.Choice(title=u"Selection",
    ...                                                           source=ItalianCitiesSourceBinder()))
    ...     favourite_city = schema.Choice(title=u"Favourite city",
    ...                                    source=ItalianCitiesSourceBinder())
    ...     visited_cities = schema.List(title=u"Visited cities",
    ...                                  value_type=schema.Choice(title=u"Selection",
    ...                                                           source=ItalianCitiesSourceBinder()))

    >>> from z3c.form.interfaces import IFieldsForm
    >>> from zope.interface import implements
    >>> class CitiesForm(form.Form):
    ...     implements(ICities)
    ...     fields = field.Fields(ICities)
    ...     fields['afavourite_city'].widgetFactory = AjaxChosenFieldWidget
    ...     fields['avisited_cities'].widgetFactory = AjaxChosenMultiFieldWidget
    ...     fields['favourite_city'].widgetFactory = ChosenFieldWidget
    ...     fields['visited_cities'].widgetFactory = ChosenMultiFieldWidget
    ...
    ...     @button.buttonAndHandler(u'Apply')
    ...     def handleApply(self, action):
    ...         data, errors = self.extractData()
    ...         print "Submitted data:", data

    >>> form_view = wrap_form(CitiesForm)

    >>> from zope.component import provideAdapter
    >>> from zope.publisher.interfaces.browser import IBrowserRequest
    >>> from zope.interface import Interface

    >>> provideAdapter(adapts=(ICities, IBrowserRequest),
    ...                provides=Interface,
    ...                factory=form_view,
    ...                name=u"cities-form")

    >>> from OFS.SimpleItem import SimpleItem
    >>> class Bar(SimpleItem):
    ...     implements(ICities)
    ...
    ...     def __init__(self, id):
    ...         self.id = id
    ...         self.favourite_city = None
    ...         self.visited_cities = []
    ...         self.afavourite_city = None
    ...         self.avisited_cities = []
    ...     def absolute_url(self):
    ...         return 'http://foo/bar'

Let us now look up the form and attempt to render the widget.

    >>> from zope.component import getMultiAdapter
    >>> context = Bar('bar')

Simulates traversal:

    >>> request = make_request('bar/@@cities-form')
    >>> from Testing.makerequest import makerequest
    >>> context = makerequest(context)
    >>> form_view = getMultiAdapter((context, request), name=u"cities-form")
    >>> form_view.__name__ = 'cities-form'

Simulates partial rendering:

    >>> form = form_view.form_instance
    >>> form.__name__ = 'cities-form'
    >>> form.update()

    >>> print form.widgets['favourite_city'].render().replace("...", "") # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
    <script type="text/javascript">    (function($) {
            $().ready(function() {
                $('#form-widgets-favourite_city-select').data('klass','chosen-selection-widget required choice-field').data('title','None');
                $('#form-widgets-favourite_city-select').chosen({
                    allow_single_deselect: false,
                    no_results_text: 'No results found'
                });
    <BLANKLINE>
            });
        })(jQuery);
        </script>
    <div id="form-widgets-favourite_city-chosen" class="chosen-selection-widget required choice-field">
      <select id="form-widgets-favourite_city-select" style="width:280px;" onselect="" data-placeholder="Select a value here" name="form.widgets.favourite_city:list">
    <BLANKLINE>
          <option id="form-widgets-favourite_city-novalue" value="(nothing)" selected="selected">Select a value here</option>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <option id="form-widgets-favourite_city-0" value="bologna">Bologna</option>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <option id="form-widgets-favourite_city-1" value="palermo">Palermo</option>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <option id="form-widgets-favourite_city-2" value="sorrento">Sorrento</option>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
          <option id="form-widgets-favourite_city-3" value="torino">Torino</option>
    <BLANKLINE>
      </select>
      <input name="form.widgets.favourite_city-empty-marker" type="hidden" value="1" />
    </div>
    <BLANKLINE>

We can see that the rendered JavaScript is expecting to call a view for ajax widgets
like this:

    >>> widget = form.widgets['afavourite_city']
    >>> context.REQUEST._script = 'bar/@@cities-form/++widget++form.widgets.avisited_cities/@@chosen-autocomplete-search'.split('/')
    >>> context.REQUEST._resetURLS()
    >>> context.REQUEST.form['term'] = 'or'
    >>> search_view = getMultiAdapter((widget, context.REQUEST), name=u'chosen-autocomplete-search')

The results are a json tuple list of tokens:

    >>> print search_view()
    [["sorrento","Sorrento"],["torino","Torino"]]

At first we didnt set anything in the request, we are missing fields

    >>> form.update()
    >>> data, errors = form.extractData()
    >>> len(errors)
    3
    >>> form.request.form.update({
    ...  "form.buttons.apply" : "Apply",
    ...  "form.widgets.visited_cities" : ["palermo", "bologna"],
    ...  "form.widgets.avisited_cities" : ["palermo", "bologna"],
    ...  "form.widgets.afavourite_city" :"bologna",
    ...  "form.widgets.favourite_city" : "palermo",
    ... })
    >>> form.update() # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    Submitted data:...
    >>> data, errors = form.extractData()
    >>> items = data.items()
    >>> items.sort(key=lambda x:x[0])
    >>> pprint(items)
    [('afavourite_city', u'bologna'),
     ('avisited_cities', [u'palermo', u'bologna']),
     ('favourite_city', u'palermo'),
     ('visited_cities', [u'palermo', u'bologna'])]



Our values are marked as selected

    >>> results = form.render().replace('...', '')
    >>> False not in [
    ... (it in results)
    ... for it in ['id="form-widgets-visited_cities-0" value="bologna" selected="selected">Bologna',
    ...            'id="form-widgets-visited_cities-1" value="palermo" selected="selected">Palermo']]
    True

Our widget also handle display mode

    >>> form.widgets['favourite_city'].mode = 'display'
    >>> print form.widgets['favourite_city'].render().strip()
    <span id="form-widgets-favourite_city" class="chosen-selection-widget required choice-field" style="width:280px;"><span class="selected-option">Palermo</span></span>

    >>> form.widgets['visited_cities'].mode = 'display'
    >>> print form.widgets['visited_cities'].render().strip()
    <span id="form-widgets-visited_cities" class="chosen-multiselection-widget required list-field" style="width:280px;"><span class="selected-option">Palermo</span>, <span class="selected-option">Bologna</span></span>

Our widget also handle hidden mode

    >>> form.widgets['favourite_city'].mode = 'hidden'
    >>> print form.widgets['favourite_city'].render().strip()
    <input id="form-widgets-favourite_city-1" name="form.widgets.favourite_city:list" value="palermo" class="hidden-widget" type="hidden" />
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <input name="form.widgets.favourite_city-empty-marker" type="hidden" value="1" />

    >>> form.widgets['visited_cities'].mode = 'hidden'
    >>> print form.widgets['visited_cities'].render().strip()
    <input id="form-widgets-visited_cities-0" name="form.widgets.visited_cities:list" value="bologna" class="hidden-widget" type="hidden" />
    <BLANKLINE>
    <BLANKLINE>
      <input id="form-widgets-visited_cities-1" name="form.widgets.visited_cities:list" value="palermo" class="hidden-widget" type="hidden" />
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <input name="form.widgets.visited_cities-empty-marker" type="hidden" value="1" />

