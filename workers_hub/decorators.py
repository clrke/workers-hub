from django.contrib.auth.models import User
from workers_hub.exceptions import MissingApiKeyException, UnauthorizedApiKeyException


def customer_api_confirmation(view_func):
    def wrapped_view(request, *args, **kwargs):
        data = request.META

        if 'HTTP_X_AUTHORIZATION' not in data:
            raise MissingApiKeyException('Please specify X-Authorization.')

        if not User.objects.filter(id=data['HTTP_X_AUTHORIZATION']).exists():
            raise UnauthorizedApiKeyException('Incorrect X-Authorization.')

        return view_func(request, *args, **kwargs)
    return wrapped_view
