import json
from django.http import JsonResponse
from workers_hub.decorators import worker_api_confirmation
from workers_hub.exceptions import MissingArgumentsException
from workers_hub.models import Proposal
from workers_hub.models import Request


@worker_api_confirmation
def proposal(req, request_id):
    if req.method == 'POST':
        try:
            data = json.loads(req.body)
        except ValueError:
            data = req.POST

        if 'message' not in data:
            raise MissingArgumentsException('message')
        if 'cost' not in data:
            raise MissingArgumentsException('cost')

        worker = req.worker
        request = Request.objects.get(id=request_id)

        proposal = Proposal(cost=data['cost'], message=data['message'], worker=worker, status=Proposal.OPEN,
                            request=request)

        proposal.save()

        return JsonResponse({
            'status': 'success',
            'message': proposal.worker.user.username,
        })
    elif req.method == 'DELETE':
        proposal = Proposal.objects.get(id=request_id)
        if proposal.status == Proposal.OPEN:
            proposal.delete()

            return JsonResponse({
                'status': 'success',
                'message': proposal.request.subject,
            })
        else:
            response = JsonResponse({
                'status': 'error',
                'message': 'Only OPEN bids can be cancelled.',
            })
            response.status_code = 404
            return response
