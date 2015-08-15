import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from workers_hub.decorators import worker_api_confirmation
from workers_hub.exceptions import MissingArgumentsException
from workers_hub.models import Worker, Proposal
from workers_hub.models import Request


@worker_api_confirmation
def create_proposal(request, request_id):
    try:
        data = json.loads(request.body)
    except ValueError:
        data = request.POST

    if 'message' not in data:
        raise MissingArgumentsException('message')
    if 'cost' not in data:
        raise MissingArgumentsException('cost')

    worker = request.worker
    request = Request.objects.get(id=request_id)

    proposal = Proposal(cost=data['cost'], message=data['message'], worker=worker, status=Proposal.OPEN, request=request)

    proposal.save()

    return JsonResponse({
        'status': 'success',
        'message': proposal.worker.user.username,
    })
