from django.core.urlresolvers import resolve, reverse
from rest_framework import serializers as ser


class RelationshipField(ser.HyperlinkedIdentityField):
    """
    RelationshipField that permits the return of both self and related links, along with optional
    meta information. ::
        children = RelationshipField(
            related_view='nodes:node-children',
            related_view_kwargs={'node_id': '<pk>'},
            self_view='nodes:node-node-children-relationship',
            self_view_kwargs={'node_id': '<pk>'},
            related_meta={'count': 'get_node_count'}
        )
    The lookup field must be surrounded in angular brackets to find the attribute on the target. Otherwise, the lookup
    field will be returned verbatim. ::
        wiki_home = RelationshipField(
            related_view='addon:addon-detail',
            related_view_kwargs={'node_id': '<_id>', 'provider': 'wiki'},
        )
    '_id' is enclosed in angular brackets, but 'wiki' is not. 'id' will be looked up on the target, but 'wiki' will not.
     The serialized result would be '/nodes/abc12/addons/wiki'.
    Field can handle nested attributes: ::
        wiki_home = RelationshipField(
            related_view='wiki:wiki-detail',
            related_view_kwargs={'node_id': '<_id>', 'wiki_id': '<wiki_pages_current.home>'}
        )
    Field can handle a filter_key, which operates as the source field (but
    is named differently to not interfere with HyperLinkedIdentifyField's source
    The ``filter_key`` argument defines the Mongo key (or ODM field name) to filter on
    when using the ``FilterMixin`` on a view. ::
        parent = RelationshipField(
            related_view='nodes:node-detail',
            related_view_kwargs={'node_id': '<parent_node._id>'},
            filter_key='parent_node'
        )
    Field can include optional filters:
    Example:
    replies = RelationshipField(
        self_view='nodes:node-comments',
        self_view_kwargs={'node_id': '<node._id>'},
        filter={'target': '<pk>'})
    )
    """
    json_api_link = True  # serializes to a links object

    def __init__(self, related_view=None, related_view_kwargs=None, self_view=None, self_view_kwargs=None,
                 self_meta=None, related_meta=None, always_embed=False, filter=None, filter_key=None, **kwargs):
        related_view = related_view
        self_view = self_view
        related_kwargs = related_view_kwargs
        self_kwargs = self_view_kwargs
        self.views = {'related': related_view, 'self': self_view}
        self.view_kwargs = {'related': related_kwargs, 'self': self_kwargs}
        self.related_meta = related_meta
        self.self_meta = self_meta
        self.always_embed = always_embed
        self.filter = filter
        self.filter_key = filter_key

        assert (related_view is not None or self_view is not None), 'Self or related view must be specified.'
        if related_view:
            assert related_kwargs is not None, 'Must provide related view kwargs.'
            if not callable(related_kwargs):
                assert isinstance(related_kwargs,
                                  dict), "Related view kwargs must have format {'lookup_url_kwarg: lookup_field}."
        if self_view:
            assert self_kwargs is not None, 'Must provide self view kwargs.'
            assert isinstance(self_kwargs, dict), "Self view kwargs must have format {'lookup_url_kwarg: lookup_field}."

        view_name = related_view
        if view_name:
            lookup_kwargs = related_kwargs
        else:
            view_name = self_view
            lookup_kwargs = self_kwargs

        super(RelationshipField, self).__init__(view_name, lookup_url_kwarg=lookup_kwargs, **kwargs)

    def resolve(self, resource, field_name):
        """
        Resolves the view when embedding.
        """
        lookup_url_kwarg = self.lookup_url_kwarg
        if callable(lookup_url_kwarg):
            lookup_url_kwarg = lookup_url_kwarg(getattr(resource, field_name))

        kwargs = {attr_name: self.lookup_attribute(resource, attr) for (attr_name, attr) in
                  lookup_url_kwarg.items()}
        view = self.view_name
        if callable(self.view_name):
            view = view(getattr(resource, field_name))
        return resolve(
            reverse(
                view,
                kwargs=kwargs
            )
        )

    # def process_related_counts_parameters(self, params, value):
    #     """
    #     Processes related_counts parameter.
    #     Can either be a True/False value for fetching counts on all fields, or a comma-separated list for specifying
    #     individual fields.  Ensures field for which we are requesting counts is a relationship field.
    #     """
    #     if utils.is_truthy(params) or utils.is_falsy(params):
    #         return params
    #
    #     field_counts_requested = [val for val in params.split(',')]
    #
    #     countable_fields = {field for field in self.parent.fields if
    #                         getattr(self.parent.fields[field], 'json_api_link', False) or
    #                         getattr(getattr(self.parent.fields[field], 'field', None), 'json_api_link', None)}
    #     for count_field in field_counts_requested:
    #         # Some fields will hide relationships, e.g. HideIfWithdrawal
    #         # Ignore related_counts for these fields
    #         fetched_field = self.parent.fields.get(count_field)
    #
    #         hidden = fetched_field and isinstance(fetched_field, HideIfWithdrawal) and getattr(value, 'is_retracted', False)
    #
    #         if not hidden and count_field not in countable_fields:
    #             raise InvalidQueryStringError(
    #                 detail="Acceptable values for the related_counts query param are 'true', 'false', or any of the relationship fields; got '{0}'".format(
    #                     params),
    #                 parameter='related_counts'
    #             )
    #     return field_counts_requested
    #
    # def get_meta_information(self, meta_data, value):
    #     """
    #     For retrieving meta values, otherwise returns {}
    #     """
    #     meta = {}
    #     for key in meta_data or {}:
    #         if key == 'count' or key == 'unread':
    #             show_related_counts = self.context['request'].query_params.get('related_counts', False)
    #             if self.context['request'].parser_context.get('kwargs'):
    #                 if self.context['request'].parser_context['kwargs'].get('is_embedded'):
    #                     show_related_counts = False
    #             field_counts_requested = self.process_related_counts_parameters(show_related_counts, value)
    #
    #             if utils.is_truthy(show_related_counts):
    #                 meta[key] = website_utils.rapply(meta_data[key], _url_val, obj=value, serializer=self.parent)
    #             elif utils.is_falsy(show_related_counts):
    #                 continue
    #             elif self.field_name in field_counts_requested:
    #                 meta[key] = website_utils.rapply(meta_data[key], _url_val, obj=value, serializer=self.parent)
    #             else:
    #                 continue
    #         else:
    #             meta[key] = website_utils.rapply(meta_data[key], _url_val, obj=value, serializer=self.parent)
    #     return meta
    #
    # def lookup_attribute(self, obj, lookup_field):
    #     """
    #     Returns attribute from target object unless attribute surrounded in angular brackets where it returns the lookup field.
    #     Also handles the lookup of nested attributes.
    #     """
    #     bracket_check = _tpl(lookup_field)
    #     if bracket_check:
    #         source_attrs = bracket_check.split('.')
    #         # If you are using a nested attribute for lookup, and you get the attribute wrong, you will not get an
    #         # error message, you will just not see that field. This allows us to have slightly more dynamic use of
    #         # nested attributes in relationship fields.
    #         try:
    #             return_val = get_nested_attributes(obj, source_attrs)
    #         except KeyError:
    #             return None
    #         return return_val
    #
    #     return lookup_field
    #
    # def kwargs_lookup(self, obj, kwargs_dict):
    #     """
    #     For returning kwargs dictionary of format {"lookup_url_kwarg": lookup_value}
    #     """
    #     if callable(kwargs_dict):
    #         kwargs_dict = kwargs_dict(obj)
    #
    #     kwargs_retrieval = {}
    #     for lookup_url_kwarg, lookup_field in kwargs_dict.items():
    #         try:
    #             lookup_value = self.lookup_attribute(obj, lookup_field)
    #         except AttributeError as exc:
    #             raise AssertionError(exc)
    #         if lookup_value is None:
    #             return None
    #         kwargs_retrieval[lookup_url_kwarg] = lookup_value
    #     return kwargs_retrieval

    # Overrides HyperlinkedIdentityField
    def get_url(self, obj, view_name, request, format):
        urls = {}
        for view_name, view in self.views.items():
            if view is None:
                urls[view_name] = {}
            else:
                kwargs = self.kwargs_lookup(obj, self.view_kwargs[view_name])
                if kwargs is None:
                    urls[view_name] = {}
                else:
                    if callable(view):
                        view = view(getattr(obj, self.field_name))
                    url = self.reverse(view, kwargs=kwargs, request=request, format=format)
                    if self.filter:
                        formatted_filter = self.format_filter(obj)
                        if formatted_filter:
                            url = '{}?filter{}'.format(url, formatted_filter)
                        else:
                            url = None
                    urls[view_name] = url
        if not urls['self'] and not urls['related']:
            urls = None
        return urls

    def format_filter(self, obj):
        qd = QueryDict(mutable=True)
        filter_fields = self.filter.keys()
        for field_name in filter_fields:
            try:
                # check if serializer method passed in
                serializer_method = getattr(self.parent, self.filter[field_name])
            except AttributeError:
                value = self.lookup_attribute(obj, self.filter[field_name])
            else:
                value = serializer_method(obj)
            if not value:
                continue
            qd.update({'[{}]'.format(field_name): value})
        if not qd.keys():
            return None
        return qd.urlencode(safe=['[', ']'])

    # Overrides HyperlinkedIdentityField
    def to_representation(self, value):
        request = self.context.get('request', None)
        format = self.context.get('format', None)

        assert request is not None, (
            '`%s` requires the request in the serializer'
            " context. Add `context={'request': request}` when instantiating "
            'the serializer.' % self.__class__.__name__
        )

        # By default use whatever format is given for the current context
        # unless the target is a different type to the source.
        #
        # Eg. Consider a HyperlinkedIdentityField pointing from a json
        # representation to an html property of that representation...
        #
        # '/snippets/1/' should link to '/snippets/1/highlight/'
        # ...but...
        # '/snippets/1/.json' should link to '/snippets/1/highlight/.html'
        if format and self.format and self.format != format:
            format = self.format

        # Return the hyperlink, or error if incorrectly configured.
        try:
            url = self.get_url(value, self.view_name, request, format)
        except NoReverseMatch:
            msg = (
                'Could not resolve URL for hyperlinked relationship using '
                'view name "%s". You may have failed to include the related '
                'model in your API, or incorrectly configured the '
                '`lookup_field` attribute on this field.'
            )
            if value in ('', None):
                value_string = {'': 'the empty string', None: 'None'}[value]
                msg += (
                    ' WARNING: The value of the field on the model instance '
                    "was %s, which may be why it didn't match any "
                    'entries in your URL conf.' % value_string
                )
            raise ImproperlyConfigured(msg % self.view_name)

        if url is None:
            raise SkipField

        related_url = url['related']
        related_meta = self.get_meta_information(self.related_meta, value)
        self_url = url['self']
        self_meta = self.get_meta_information(self.self_meta, value)
        return format_relationship_links(related_url, self_url, related_meta, self_meta)