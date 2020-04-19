
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
import csv
from django.http import HttpResponse


import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Supermarket, City, Warn

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['Warn Id', 'Timestamp', 'Supermarket Id', 'Name','Address','Postcode','City'])

    data = Warn.objects.all()
    for warning in data:
        writer.writerow([warning.id,warning.timestamp,warning.supermarket.id, warning.supermarket.name, warning.supermarket.address,warning.supermarket.city.postcode,warning.supermarket.city.name])

    return response

class SupermarketList(ListView):
    model = Supermarket
    template_name = "supermarkets/market_list.html"
    context_object_name = "supermarkets"
    paginate_by = 25


class CitiesList(ListView):
    model = City
    template_name = "supermarkets/cities_list.html"
    context_object_name = "cities"
    paginate_by = 25


class ReceiveSupermarketsFromQuery(APIView):
    model = Supermarket
    context_object_name = "supermarkets"
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        size = request.GET['size']
        page = request.GET['page']
        search = request.GET['search']
        postcode = int(request.GET['postcode'])
        fromPos = 0
        toPos = 2000
        print(size)
        print(page)

        if page != None and size != None:
            fromPos = int(page) * int(size)
            toPos = ((int(page) + 1)*int(size))

        searchSplit = []
        if search is not None:
            searchSplit = search.lower().split()

        this_hour = timezone.now() 
        one_hour_later = this_hour + timedelta(hours=-1)

        markets = Supermarket.objects.filter(city__postcode=postcode)
       
        
        
        ll = []
        for markt in markets:
            currentWarnings = Warn.objects.filter(timestamp__range=(one_hour_later,this_hour),supermarket__id=markt.id).count() #,) supermarket__id=market.id
            found = True
            address = markt.address+" "+str(markt.city.postcode)+" "+markt.city.name
            print(address)
            print(postcode)
            searchMarket = (markt.name+address).lower()
            if len(searchSplit) > 0:
             for searchSplitEntry in searchSplit:
                    if not searchMarket.__contains__(searchSplitEntry):
                     found = False
            if (found): 
                ll.append({ "id":markt.id , "name":markt.name, "adress":address,"waiting_queue_last_hour": str(currentWarnings)})

        if (len(ll) < fromPos or len(ll) == 0):
            return Response([])
        if (len(ll) < toPos):
            toPos = len(ll)

        return Response(ll[fromPos:toPos])
    



@method_decorator(csrf_exempt, name='dispatch')
class WarningCreateView(APIView):
    model = Supermarket
    context_object_name = "supermarkets"
    renderer_classes = [JSONRenderer]

    def get_object(self, pk):
        try:
            return Supermarket.objects.get(pk=pk)
        except Supermarket.DoesNotExist:
            raise Http404


    @csrf_exempt
    def post(self, request, pk, format=None):
        market = self.get_object(pk)
        newWaring = Warn()
        newWaring.supermarket = market
        newWaring.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

#     model = Warn

#     def post(self, request, *args, **kwargs):
        
#         hashed = hashlib.md5(("-".join([str(x) for x in request.headers])+request.remote_addr).encode("utf-8")).digest()
#         dtime = datetime.datetime.now()
        
#         supermarket = supermarkets_by_id[int(id)]
#         w = Warn(hashed,dtime)

#         supermarket.delete_old_warnings()
#         accepted = supermarket.accept_warning(w)
#         return reverse('search')







