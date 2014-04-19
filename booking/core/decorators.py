from django.http import Http404


def scientist_required(function=None):
    def _decorator(view_function):
        def _view(request, *args, **kwargs):
            if not request.user.userprofile.is_scientist:
                raise Http404
            return view_function(request, *args, **kwargs)

        _view.__name__ = view_function.__name__
        _view.__dict__ = view_function.__dict__
        _view.__doc__ = view_function.__doc__
        _view.__module__ = view_function.__module__
        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def participant_required(function=None):
    def _decorator(view_function):
        def _view(request, *args, **kwargs):
            if not request.user.userprofile.is_participant:
                raise Http404
            return view_function(request, *args, **kwargs)

        _view.__name__ = view_function.__name__
        _view.__dict__ = view_function.__dict__
        _view.__doc__ = view_function.__doc__
        _view.__module__ = view_function.__module__
        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def department_required(function=None):
    def _decorator(view_function):
        def _view(request, *args, **kwargs):
            if not request.user.userprofile.is_department:
                raise Http404
            return view_function(request, *args, **kwargs)

        _view.__name__ = view_function.__name__
        _view.__dict__ = view_function.__dict__
        _view.__doc__ = view_function.__doc__
        _view.__module__ = view_function.__module__
        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


def staff_required(function=None):
    def _decorator(view_function):
        def _view(request, *args, **kwargs):
            if not request.user.is_staff:
                raise Http404
            return view_function(request, *args, **kwargs)

        _view.__name__ = view_function.__name__
        _view.__dict__ = view_function.__dict__
        _view.__doc__ = view_function.__doc__
        _view.__module__ = view_function.__module__
        return _view

    if function is None:
        return _decorator
    else:
        return _decorator(function)