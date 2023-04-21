from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        app_secret_token = request.headers.get('CL-X-TOKEN')
        account = Account.objects.get(app_secret_token=app_secret_token)
        data = request.json()
        for destination in account.destination_set.all():
            headers = destination.headers
            headers['Content-Type'] = 'application/json'
            response = requests.request(destination.http_method, destination.url, headers=headers, json=data)
            print(response.status_code)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Destination
import requests

@csrf_exempt
def account_list(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        data = [{'id': account.id, 'email': account.email, 'account_id': account.account_id, 'account_name': account.account_name, 'website': account.website} for account in accounts]
        return JsonResponse({'data': data})
    elif request.method == 'POST':
        data = request.json()
        account = Account.objects.create(email=data['email'], account_id=data['account_id'], account_name=data['account_name'], app_secret_token=data['app_secret_token'], website=data.get('website'))
        return JsonResponse({'id': account.id})

@csrf_exempt
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == 'GET':
        data = {'id': account.id, 'email': account.email, 'account_id': account.account_id, 'account_name': account.account_name, 'website': account.website}
        return JsonResponse({'data': data})
    elif request.method == 'PUT':
        data = request.json()
        account.email = data.get('email', account.email)
        account.account_id = data.get('account_id', account.account_id)
        account.account_name = data.get('account_name', account.account_name)
        account.app_secret_token = data.get('app_secret_token', account.app_secret_token)
        account.website = data.get('website', account.website)
        account.save()
        return JsonResponse({'status': 'success'})
    elif request.method == 'DELETE':
        account.delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def destination_list(request):
    if request.method == 'GET':
        destinations = Destination.objects.all()
        data = [{'id': destination.id, 'account_id': destination.account_id, 'url': destination.url, 'http_method': destination.http_method, 'headers': destination.headers} for destination in destinations]
        return JsonResponse({'data': data})
    elif request.method == 'POST':
        data = request.json()
        destination = Destination.objects.create(account_id=data['account_id'], url=data['url'], http_method=data['http_method'], headers=data['headers'])
        return JsonResponse({'id': destination.id})

@csrf_exempt
def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    if request.method == 'GET':
        data = {'id': destination.id, 'account_id': destination.account_id, 'url': destination.url, 'http_method': destination.http_method, 'headers': destination.headers}
        return JsonResponse({'data': data})
    elif request.method == 'PUT':
        data = request.json()
        destination.account_id = data.get('account_id', destination.account_id)
        destination.url = data.get('url', destination.url)
        destination.http_method = data.get('http_method', destination.http_method)
        destination.headers = data.get('headers', destination.headers)
        destination.save()
        return JsonResponse({'status': 'success'})
    elif request.method == 'DELETE':
        destination.delete()
        return JsonResponse({'status': 'success'})
    


@csrf_exempt
def destination_list_for_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    destinations = account.destination_set.all()
    data = [{'id': destination.id, 'url': destination.url, 'http_method': destination.http_method, 'headers': destination.headers} for destination in destinations]
    return JsonResponse({'data': data})

@csrf_exempt
def incoming_data(request):
    if request.method == 'POST':
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return JsonResponse({'status': 'Un Authenticate'})
        try:
            data = request.json()
        except ValueError:
            return JsonResponse({'status': 'Invalid Data'})
        account = get_object_or_404(Account, app_secret_token=app_secret_token)
        for destination in account.destination_set.all():
            headers = destination.headers
            headers['Content-Type'] = 'application/json'
            response = requests.request(destination.http_method, destination.url, headers=headers, json=data)
            print(response.status_code)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})