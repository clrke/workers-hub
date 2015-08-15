import json
from django.http import JsonResponse
from workers_hub.decorators import customer_api_confirmation
from workers_hub.models import Request, Worker, Profession, Image, Proposal, Review


@customer_api_confirmation
def request(req):
    if req.method == 'GET':
        user = req.user

        return JsonResponse({
            'status': 'success',
            'message': [{'subject': request.subject,
                         'description': request.description,
                         'range_min': request.range_min,
                         'range_max': request.range_max,
                         'tags': [profession.name for profession in request.professions.all()],
                         'images': [image.url for image in request.image_set.all()],
                         'status': request.status,
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

        request = Request(subject=subject, range_min=range_min, range_max=range_max, description=description, user=user,
                          status=Request.OPEN)
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
                             'reviews': [review.message for review in reviews if review.type == Review.CUSTOMER_WORKER]
                         }})


@customer_api_confirmation
def accept_proposal(request, request_id, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    request = Request.objects.get(id=request_id)
    proposal.status = 'ACCEPTED'
    request.status = 'ACCEPTED'
    proposal.save()
    request.save()
    return JsonResponse({'status': 'success'})


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


@customer_api_confirmation
def cancel_request(request, request_id):
    if request.method == 'DELETE':
        req = request.user.request_set.get(id=request_id)

        if req.status == Request.OPEN:
            req.delete()

            return JsonResponse({
                'status': 'success',
                'message': req.subject
            })

        else:
            response = JsonResponse({
                'status': 'error',
                'message': 'Cannot cancel once a bidder has been accepted.',
            })
            response.status_code = 404
            return response

    response = JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.',
    })
    response.status_code = 404


@customer_api_confirmation
def write_review(req, request_id):
    if req.method == 'POST':
        try:
            data = json.loads(req.body)
        except ValueError:
            data = req.POST

        user = req.user
        worker = Worker.objects.get(id=data['worker_id'])
        rating = data['rating']
        type = Review.CUSTOMER_WORKER
        message = data['message']

        review = Review(user=user, worker=worker, rating=rating, type=type, message=message)

        review.save()

        request = Request.objects.get(id=request_id)
        request.status = Request.CLOSED
        request.save()

        return JsonResponse({
            'status': 'success',
            'message': review.user.username
        })

    response = JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })
    response.status_code = 405

    return response
