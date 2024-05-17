from django.shortcuts import redirect

def firebase_login_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func