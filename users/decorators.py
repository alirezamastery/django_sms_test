from functools import wraps
# from django.utils.decorators import available_attrs
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import Http404


User = get_user_model()


# noinspection PyPep8Naming
class projects_panel(object):

    def __init__(self, permissions=None):
        self.permissions = permissions

    def __call__(self, view_func):
        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            user = request.user
            user_obj = User.objects.get(username=user)
            project_membership_qs = user_obj.projectmembership_set.all().order_by('pk')
            if project_membership_qs.count() == 0:
                return Http404('No projects found')
            setattr(request, 'memberships', project_membership_qs)

            for project_membership in project_membership_qs:
                if project_membership.is_current:
                    setattr(request, 'current_membership', project_membership)
            if not hasattr(request, 'current_membership'):
                setattr(request, 'current_membership', project_membership_qs[0])

            setattr(request, 'project', request.current_membership.project)

            if self.permissions:
                for permission in self.permissions:
                    if not request.current_membership.has_permission(permission):
                        raise PermissionDenied()

            return view_func(request, *args, **kwargs)

        return _wrapper_view
