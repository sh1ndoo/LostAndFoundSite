from django.contrib.auth.mixins import *

from apps.things.service import check_owner


class OwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        check_owner(self, request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)