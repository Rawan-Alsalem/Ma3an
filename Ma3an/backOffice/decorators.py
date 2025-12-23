from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url="/admin/login/")

        if not request.user.is_superuser:
            return HttpResponseForbidden("Admins only.")

        return view_func(request, *args, **kwargs)
    return wrapper
