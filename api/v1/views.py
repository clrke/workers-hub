from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    data = request.POST
    username = data['username']
    password = data['password']

    from django.core.exceptions import ObjectDoesNotExist
    try:
        user = User.objects.get(username=username)

        if user.check_password(password):
            return JsonResponse({
                'status': 'success',
                'message': user.id
            })
        else:
            raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        response = JsonResponse({
            'status': 'error',
            'message': 'Invalid username or password'
        })
        response.status_code = 404

        return response
