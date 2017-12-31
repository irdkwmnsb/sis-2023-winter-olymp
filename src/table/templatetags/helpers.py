from django.template.defaulttags import register


@register.filter
def get_item_or_empty(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


@register.filter
def select_resource_name(resource, count):
    return resource.get_name_for_count(count)


@register.filter
def times(number):
    return range(number)
