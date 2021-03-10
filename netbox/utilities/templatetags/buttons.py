from django import template
from django.urls import reverse

from extras.models import ExportTemplate
from utilities.utils import prepare_cloned_fields

from .helpers import _resolve_namespace

register = template.Library()


def _get_listviewname(instance):
    app_label = _resolve_namespace(instance)
    return f'{app_label}:{instance._meta.model_name}_list'


def _get_viewname(instance, action):
    """
    Return the appropriate viewname for adding, editing, or deleting an instance or viewing.
    """

    # Validate action
    assert action in ('add', 'edit', 'delete')
    app_label = _resolve_namespace(instance)
    viewname = f'{app_label}:{instance._meta.model_name}_{action}'

    return viewname

#
# Table buttons
#

@register.inclusion_tag('buttons/tr_edit.html')
def tr_edit_button(instance, extra=None):
    viewname = _get_viewname(instance, 'edit')
    base_url = reverse(_get_listviewname(instance))
    url = reverse(viewname, kwargs={'pk': instance.pk})
    url = f'{url}?return_url={base_url}'

    if extra is not None:
        url = f'{url}{extra}'

    return {
        'url': url,
    }

@register.inclusion_tag('buttons/tr_delete.html')
def tr_delete_button(instance, extra=None):
    viewname = _get_viewname(instance, 'delete')
    base_url = reverse(_get_listviewname(instance))
    url = reverse(viewname, kwargs={'pk': instance.pk})
    url = f'{url}?return_url={base_url}'

    if extra is not None:
        url = f'{url}{extra}'

    return {
        'url': url,
    }

@register.inclusion_tag('buttons/tr_changelog.html')
def tr_changelog_button(instance):
    app_label = _resolve_namespace(instance)
    viewname = f'{app_label}:{instance._meta.model_name}_changelog'
    url = reverse(viewname, kwargs={'pk': instance.pk})

    return {
        'url': url,
    }



#
# Instance buttons
#

@register.inclusion_tag('buttons/clone.html')
def clone_button(instance):
    url = reverse(_get_viewname(instance, 'add'))

    # Populate cloned field values
    param_string = prepare_cloned_fields(instance)
    if param_string:
        url = f'{url}?{param_string}'

    return {
        'url': url,
    }


@register.inclusion_tag('buttons/edit.html')
def edit_button(instance):
    viewname = _get_viewname(instance, 'edit')
    url = reverse(viewname, kwargs={'pk': instance.pk})

    return {
        'url': url,
    }


@register.inclusion_tag('buttons/delete.html')
def delete_button(instance):
    viewname = _get_viewname(instance, 'delete')
    url = reverse(viewname, kwargs={'pk': instance.pk})

    return {
        'url': url,
    }


#
# List buttons
#

@register.inclusion_tag('buttons/add.html')
def add_button(url):
    url = reverse(url)

    return {
        'add_url': url,
    }


@register.inclusion_tag('buttons/import.html')
def import_button(url):

    return {
        'import_url': url,
    }


@register.inclusion_tag('buttons/export.html', takes_context=True)
def export_button(context, content_type=None):
    if content_type is not None:
        user = context['request'].user
        export_templates = ExportTemplate.objects.restrict(user, 'view').filter(content_type=content_type)
    else:
        export_templates = []

    return {
        'url_params': context['request'].GET,
        'export_templates': export_templates,
    }
