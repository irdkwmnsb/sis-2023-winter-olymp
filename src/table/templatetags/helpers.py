import datetime
import calendar

from django.template.defaultfilters import stringfilter
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


@register.filter
def age(value):
    now = datetime.datetime.now(datetime.timezone.utc)
    # FIX BUG ON OUR EJUDGE SERVER: TIME DESYNCHRONIZATION FOR ONE HOUR :(
    value = datetime.datetime.fromtimestamp(value, datetime.timezone.utc)# + datetime.timedelta(hours=1)
    try:
        difference = now - value
    except:
        return value

    if difference <= datetime.timedelta(minutes=1):
        return 'меньше минуты назад'
    return '%(time)s назад' % {'time': timesince(value, now).split(', ')[0]}


TIMESINCE_CHUNKS = (
    (60 * 60, ('%d час', '%d часа', '%d часов')),
    (60, ('%d минуту', '%d минуты', '%d минут'))
)


def timesince(d, now=None, reversed=False):
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
    then "0 minutes" is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    Adapted from
    http://web.archive.org/web/20060617175230/http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
    """
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.datetime.now()

    delta = (d - now) if reversed else (now - d)

    # Deal with leapyears by subtracing the number of leapdays
    delta -= datetime.timedelta(calendar.leapdays(d.year, now.year))

    # ignore microseconds
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return 'только что'
    for i, (seconds, names) in enumerate(TIMESINCE_CHUNKS):
        count = since // seconds
        if count != 0:
            break
    result = get_name_by_count(names, count)
    if i + 1 < len(TIMESINCE_CHUNKS):
        # Now get the second item
        seconds2, names2 = TIMESINCE_CHUNKS[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            result += ', ' + get_name_by_count(names2, count2)
    return result


def get_name_by_count(names, count):
    last = count % 10
    prelast = (count // 10) % 10
    if prelast != 1 and 2 <= last <= 4:
        return names[1] % count
    if 5 <= last <= 9 or last == 0:
        return names[2] % count
    if prelast == 1:
        return names[2] % count
    return names[0] % count


@register.filter
def get_team_name(full_name: str):
    idx = full_name.rfind('(')
    if idx > 0:
        return full_name[:idx].strip()
    return full_name


@register.filter(is_safe=True)
@stringfilter
def lowerfirst(value):
    """Un-capitalizes the first character of the value."""
    return value and value[0].lower() + value[1:]
