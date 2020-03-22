
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Supermarket, City


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
    template_name = "supermarkets/market_list.html"
    paginate_by = 25
    context_object_name = "supermarkets"

    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        size = self.kwargs.get('size', None)
        page = self.kwargs.get('page', None)
        search = self.kwargs.get('search', None)
        postcode = self.kwargs.get('postcode', None)

        if search is not None:
            search_split = search.lower().split()

        markets = Supermarket.objects.all()
        
        ll = []
        for markt in markets:
            found = True
            #address = "".join(markt.adress,markt.c)
            searchMarket = (markt.name+markt.adress).lower()
            if len(searchSplit) > 0:
             for searchSplitEntry in searchSplit:
                    if not searchMarket.__contains__(searchSplitEntry):
                     found = False
            if (postcode == markt.postcode and found): 
                ll.append({ "id":markt.id , "name":markt.name, "adress":markt.adress+" "+markt.ci,"waiting_queue_last_hour":markt.list_of_warnings.__len__()})

        if (len(ll) < fromPos or len(ll) == 0):
            return Response(json.dumps([]),mimetype="application/json")
        if (len(ll) < toPos):
            toPos = len(ll)

        # .values('address','id', 'name')
        #serialized_q = json.dumps(list(filtered), cls=DjangoJSONEncoder)
        #JsonResponse(serialized_q)

        return Response(ll)
    


class WarningCreateView(CreateView):
    pass
#     model = Warn

#     def post(self, request, *args, **kwargs):
        
#         hashed = hashlib.md5(("-".join([str(x) for x in request.headers])+request.remote_addr).encode("utf-8")).digest()
#         dtime = datetime.datetime.now()
        
#         supermarket = supermarkets_by_id[int(id)]
#         w = Warn(hashed,dtime)

#         supermarket.delete_old_warnings()
#         accepted = supermarket.accept_warning(w)
#         return reverse('search')







