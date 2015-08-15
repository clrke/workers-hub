import json
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from workers_hub.exceptions import TypeNotSpecifiedException, TypeNotValidException


@csrf_exempt
def login(request):
    try:
        data = json.loads(request.body)
    except ValueError:
        data = request.POST

    try:
        if 'type' not in request.GET:
            raise TypeNotSpecifiedException()

        username = data['username']
        password = data['password']

        user = User.objects.get(username=username)

        if not user.check_password(password):
            raise ObjectDoesNotExist()
        else:
            request_type = request.GET['type']

            if request_type == 'customer':
                user_id = user.id
            elif request_type == 'worker':
                user_id = user.workers_set.first().id
            else:
                raise TypeNotValidException()
            return JsonResponse({
                'status': 'success',
                'message': user_id,
            })
    except ObjectDoesNotExist:
        response = JsonResponse({
            'status': 'error',
            'message': 'Invalid username or password'
        })
        response.status_code = 404

        return response
    except TypeNotSpecifiedException:
        response = JsonResponse({
            'status': 'error',
            'message': 'Type not specified (customer or worker)'
        })
        response.status_code = 404

        return response
    except TypeNotValidException:
        response = JsonResponse({
            'status': 'error',
            'message': 'Type is not valid (customer or worker)'
        })
        response.status_code = 404

        return response
    except AttributeError:
        response = JsonResponse({
            'status': 'error',
            'message': 'User is not a worker.'
        })
        response.status_code = 404

        return response
