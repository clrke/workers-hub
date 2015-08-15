import json
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from workers_hub.exceptions import TypeNotSpecifiedException, TypeNotValidException, MissingArgumentsException
from workers_hub.models import Proposal, Request, Worker, Profession, Image


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
def request(req):
    if req.method == 'GET':
        data = req.GET
        user = User.objects.get(id=data['user_id'])

        return JsonResponse({
            'status': 'success',
            'message': [{'subject': request.subject,
                         'description': request.description,
                         'range_min': request.range_min,
                         'range_max': request.range_max,
                         'tags': [profession.name for profession in request.professions.all()],
                         } for request in user.request_set.all()],
        })
    else:

        try:
            data = json.loads(req.body)
        except ValueError:
            data = req.POST

        subject = data['subject']
        range_min = data['range_min']
        range_max = data['range_max']
        description = data['description']
        profession_names = data['tags']
        user = User.objects.get(id=data['user_id'])
        image_files = req.FILES

        request = Request(subject=subject, range_min=range_min, range_max=range_max, description=description, user=user,
                          status='OPEN')
        request.save()

        professions = []
        images = []

        for profession_name in profession_names:
            profession = Profession.objects.get(name=profession_name)
            professions.append(profession)

        available_workers = []

        for worker in Worker.objects.all():
            available = True
            for profession in professions:
                if not worker.profession_set.filter(name=profession.name).exists():
                    available = False
                    break
            if available:
                available_workers.append(worker)

        if len(available_workers) == 0:
            response = JsonResponse({
                'status': 'error',
                'message': 'No available workers for specified professions',
            })
            response.status_code = 404
            return response

        for image_file in image_files:
            image = Image(url=image_file, request=request)
            image.save()
            with open('images/%4d.jpg' % image.id, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            images.append(image)

        print professions

        for profession in professions:
            request.professions.add(profession)

        return JsonResponse({
            'status': 'ok',
            'message': request.subject
        })


@csrf_exempt
def proposal(request, request_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            data = request.POST

        if 'message' not in data:
            raise MissingArgumentsException('message')
        if 'cost' not in data:
            raise MissingArgumentsException('cost')
        if 'worker_id' not in data:
            raise MissingArgumentsException('worker_id')

        worker = Worker.objects.get(id=data['worker_id'])
        request = Request.objects.get(id=request_id)

        proposal = Proposal(cost=data['cost'], message=data['message'], worker=worker, status='OPEN', request=request)

        proposal.save()

        return JsonResponse({
            'status': 'success',
            'message': proposal.worker.user.username,
        })
    elif request.method == 'GET':
        request = Request.objects.get(id=request_id)
        proposals = request.proposal_set.all()
        return JsonResponse({
            'status': 'success',
            'message': [{
                            'worker': proposal.worker.user.username,
                            'cost': proposal.cost,
                            'message': proposal.message,
                            'request': proposal.request.subject,
                            'status': proposal.status,

                        } for proposal in proposals]
        })


@csrf_exempt
def list_proposals(request):
    workers = Worker.objects.all()
    users = [worker.user for worker in workers]

    return JsonResponse({'status': 'success',
                         'message': [{'username': user.username,
                                      'first': user.first_name,
                                      'last': user.last_name,
                                      'email': user.email,
                                      'mobile': user.userprofile_set.first().mobile_number,
                                      'reviews': [review.message for review in user.review_set.all() if
                                                  review.type == 'CUSTOMER_WORKER']
                                      } for user in users]}, safe=False)


@csrf_exempt
def show_worker(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    user = worker.user
    profile = user.userprofile_set.first()
    reviews = worker.review_set.all()
    return JsonResponse({'status': 'success',
                         'message': {
                             'username': user.username,
                             'first': user.first_name,
                             'last': user.last_name,
                             'email': user.email,
                             'mobile': profile.mobile_number,
                             'reviews': [review.message for review in reviews if review.type == 'CUSTOMER_WORKER']
                         }})


@csrf_exempt
def accept_proposal(request, request_id, proposal_id):
    # worker = Worker.objects.get(id=worker_id)
    # user = worker.user
    # profile = user.userprofile_set.first()
    # reviews = worker.review_set.all()
    return JsonResponse({'status': 'error',
                         'message': 'Not implemented yet.'})
