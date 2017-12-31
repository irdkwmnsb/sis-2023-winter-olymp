from django.template.defaulttags import register


@register.filter
def get_item_or_empty(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


@register.filter
def select_resource_name(resource, count):
    last = count % 10
    prelast = (count // 10) % 10
    if prelast != 1 and 2 <= last <= 4:
        return resource.name_acc_two
    if 5 <= last <= 9 or last == 0:
        return resource.name_acc_five
    if prelast == 1:
        return resource.name_acc_five
    return resource.name_acc_one

@register.filter
def times(number):
    return range(number)
