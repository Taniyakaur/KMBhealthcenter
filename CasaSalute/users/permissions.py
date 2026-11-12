from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def is_segreteria(user):
    return user.is_staff or hasattr(user, 'segreteria')


# Consente l'accesso solo agli utenti autenticati con uno dei ruoli indicati
# ('medico', 'infermiere', 'paziente', 'segreteria')
def ruolo_richiesto(*ruoli):
    def decorator(view):
        @login_required
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            user = request.user
            for ruolo in ruoli:
                if ruolo == 'segreteria' and is_segreteria(user):
                    return view(request, *args, **kwargs)
                if ruolo != 'segreteria' and hasattr(user, ruolo):
                    return view(request, *args, **kwargs)
            raise PermissionDenied("Non sei autorizzato ad accedere a questa pagina.")
        return wrapper
    return decorator
