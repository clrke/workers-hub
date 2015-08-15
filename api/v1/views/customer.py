import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from workers_hub.decorators import customer_api_confirmation
from workers_hub.models import Request, Worker, Profession, Image


@customer_api_confirmation
def request(req):
    if req.method == 'GET':
        data = req.GET
        user = req.user

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
        user = req.user
        image_files = req.FILES

        request = Request(subject=subject, range_min=range_min, range_max=range_max, description=description, user=user, status='OPEN')
        request.save()

        professions = []
        images = []

        for profession_name in profession_names:
            profession = Profession.objects.get(name=profession_name, approved=True)
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


@customer_api_confirmation
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


@customer_api_confirmation
def accept_proposal(request, request_id, proposal_id):
    # worker = Worker.objects.get(id=worker_id)
    # user = worker.user
    # profile = user.userprofile_set.first()
    # reviews = worker.review_set.all()
    return JsonResponse({'status': 'error',
                         'message': 'Not implemented yet.'})


@customer_api_confirmation
def list_proposals(req, request_id):
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
