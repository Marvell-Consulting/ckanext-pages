import ckan.plugins as p
from ckanext.pages.validators import page_name_validator, not_empty_if_blog
from ckanext.pages.interfaces import IPagesSchema


def default_pages_schema():
    ignore_empty = p.toolkit.get_validator('ignore_empty')
    ignore_missing = p.toolkit.get_validator('ignore_missing')
    not_empty = p.toolkit.get_validator('not_empty')
    isodate = p.toolkit.get_validator('isodate')
    name_validator = p.toolkit.get_validator('name_validator')
    try:
        unicode_safe = p.toolkit.get_validator('unicode_safe')
    except p.toolkit.UnknownValidator:
        # CKAN 2.7
        unicode_safe = unicode  # noqa: F821
    return {
        'id': [ignore_empty, unicode_safe],
        'title': [not_empty, unicode_safe],
        'short_title': [ignore_missing, unicode_safe],
        'name': [
            not_empty, unicode_safe, name_validator, page_name_validator],
        'homepage_snippet': [ignore_missing, unicode_safe],
        'content': [ignore_missing, unicode_safe],
        'show_table_of_contents': [ignore_missing,
                                   p.toolkit.get_validator('boolean_validator')],
        'page_type': [ignore_missing, unicode_safe],
        'meta_description': [ignore_missing, unicode_safe],
        'order': [ignore_missing, unicode_safe],
        'private': [ignore_missing,
                    p.toolkit.get_validator('boolean_validator')],
        'group_id': [ignore_missing, unicode_safe],
        'user_id': [ignore_missing, unicode_safe],
        'created': [ignore_missing, isodate],
        'publish_date': [
            not_empty_if_blog, ignore_missing, isodate],
    }


def update_pages_schema():
    '''
    Returns the schema for the pages fields that can be added by other
    extensions.

    By default these are the keys of the
    :py:func:`ckanext.logic.schema.default_pages_schema`.
    Extensions can add or remove keys from this schema using the
    :py:meth:`ckanext.pages.interfaces.IPagesSchema.update_pages_schema`
    method.

    :returns: a dictionary mapping fields keys to lists of validator and
    converter functions to be applied to those fields
    :rtype: dictionary
    '''

    schema = default_pages_schema()
    for plugin in p.PluginImplementations(IPagesSchema):
        if hasattr(plugin, 'update_pages_schema'):
            schema = plugin.update_pages_schema(schema)

    return schema
