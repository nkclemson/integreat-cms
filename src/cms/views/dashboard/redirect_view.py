"""
View to redirect to the correct dashboard.
"""
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name="dispatch")
class RedirectView(TemplateView):
    """
    View class representing redirection to correct dashboard

    :param: View inherits from the django TemplateView class
    :type: ~django.views.generic.TemplateView
    """

    def get(self, request, *args, **kwargs):
        """
        Select correct redirect target

        :param request: Object representing the user call
        :type request: ~django.http.HttpRequest

        :raises: ~django.core.exceptions.PermissionDenied

        :return: Redirect user to correct dashboard
        :rtype: ~django.shortcuts.redirect
        """
        user = request.user
        if user.is_superuser or user.is_staff:
            return redirect("admin_dashboard")
        regions = user.profile.regions
        if regions.exists():
            return redirect("dashboard", region_slug=regions.first().slug)
        raise PermissionDenied
