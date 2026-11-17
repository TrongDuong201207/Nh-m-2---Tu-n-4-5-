from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login

STAFF_ROLES = {'LECTURER', 'ACADEMIC_STAFF', 'ADMIN'}

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if user.is_superuser or getattr(user, 'role', None) in STAFF_ROLES:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied('Tài khoản không có quyền thực hiện thao tác này.')
    return _wrapped
