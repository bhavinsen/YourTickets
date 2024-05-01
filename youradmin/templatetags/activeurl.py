from django import template

register = template.Library()


@register.simple_tag(takes_context=True, name='activeurl')
def activeurl(context, *args, **kwargs):
    for urlname in args:
        if context['request'].resolver_match.url_name == urlname:
            return kwargs.get('cls', 'active')
    return ''
