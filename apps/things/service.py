from django.db.models import Q
from django.http import HttpResponse

from apps.things.models import Thing


def get_all_things():
    return Thing.objects.all()


def get_things_by_params(status=None, query=None, sort=None):
    things = get_all_things()
    if status:
        things = things.filter(status=status)
    if query:
        things = things.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
    if sort:
        things = things.order_by(sort)
    return things


def check_owner(self, request, *args, **kwargs):
    thing = self.get_object()
    if thing.owner != request.user:
        return HttpResponse("Вы не можете удалить эту вещь.", status=403)