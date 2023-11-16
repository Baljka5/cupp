from django.contrib.auth.mixins import AccessMixin


class GroupMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if not user.is_superuser and \
                    not user.groups.filter(name__in=['Store planner', 'Manager']).exists():
                return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class StorePlannerMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if user.groups.filter(name='Store planner').exists() and obj.created_by != user:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
