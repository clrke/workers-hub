from django.contrib.auth.models import User
from workers_hub.exceptions import MissingApiKeyException, UnauthorizedApiKeyException
from workers_hub.models import Worker


def customer_api_confirmation(view_func):
    def wrapped_view(request, *args, **kwargs):
        data = request.META

        if 'HTTP_X_AUTHORIZATION' not in data:
            raise MissingApiKeyException('Please specify X-Authorization.')

        user = User.objects.filter(id=data['HTTP_X_AUTHORIZATION'])
        if not user.exists():
            raise UnauthorizedApiKeyException('Incorrect X-Authorization.')

        request.user = user.first()

        return view_func(request, *args, **kwargs)
    return wrapped_view


def worker_api_confirmation(view_func):
    def wrapped_view(request, *args, **kwargs):
        data = request.META

        if 'HTTP_X_AUTHORIZATION' not in data:
            raise MissingApiKeyException('Please specify X-Authorization.')

        worker = Worker.objects.filter(id=data['HTTP_X_AUTHORIZATION'])
        if not worker.exists():
            raise UnauthorizedApiKeyException('Incorrect X-Authorization.')

        request.worker = worker.first()

        return view_func(request, *args, **kwargs)
    return wrapped_view
