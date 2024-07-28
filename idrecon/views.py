from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from idrecon.api.integrateIdentity.app import handler as IntegrateIdentity

class IdentityView(APIView):
    def post(self, request):
        resp = IntegrateIdentity(request)
        return JsonResponse(resp, safe=False)
    
def identity(request):
    return HttpResponse("Hello, world. This is the id api!")