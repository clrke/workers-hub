import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from workers_hub.exceptions import TypeNotSpecifiedException, TypeNotValidException
from workers_hub.models import Profession


@csrf_exempt
def login(request):
    try:
        data = json.loads(request.body)
    except ValueError:
        data = request.POST

    try:
        if 'type' not in data:
            raise TypeNotSpecifiedException()

        username = data['username']
        password = data['password']
        request_type = data['type']

        user = User.objects.get(username=username)

        if not user.check_password(password):
            raise ObjectDoesNotExist()

        if request_type == 'customer':
            user_id = user.id
        elif request_type == 'worker':
            user_id = user.workers_set.first().id
        else:
            raise TypeNotValidException()

        return JsonResponse({
            'status': 'success',
            'message': str(user_id),
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


@csrf_exempt
def professions(request):
    return JsonResponse({
        'status': 'success',
        'message': [profession.name for profession in Profession.objects.filter(approved=True)]
    })
