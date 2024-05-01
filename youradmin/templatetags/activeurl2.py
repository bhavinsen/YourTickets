from django import template
register = template.Library()


@register.simple_tag(takes_context=True, name='activeurl2')
def activeurl2(context, *args, **kwargs):
    unpacked_args = []
    for arg in args:
        if isinstance(arg, list):
            unpacked_args.extend(arg)
        else:
            unpacked_args.append(arg)
    request = context.get('request')
    class_name = kwargs.get('class_name', 'active')
    namespace = request.resolver_match.namespace
    name = request.resolver_match.url_name
    full_name = (namespace + ':' if namespace else '') + name
    if full_name in unpacked_args:
        return class_name
    return ''
