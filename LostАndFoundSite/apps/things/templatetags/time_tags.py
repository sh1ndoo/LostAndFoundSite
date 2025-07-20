from django import template
import datetime
import humanize
register = template.Library()


@register.simple_tag(takes_context=True)
def time_from_now(context):
    humanize.i18n.activate("ru_RU")
    today = datetime.datetime.now(datetime.UTC)
    thing = context.get('thing')
    delta = today - thing.created_at
    return humanize.naturaltime(delta)

