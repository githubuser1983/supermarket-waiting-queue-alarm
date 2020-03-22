
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import JsonResponse

import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Supermarket, Cities


class SupermarketList(ListView):
    model = Supermarket
    template_name = "supermarkets/market_list.html"
    context_object_name = "supermarkets"
    paginate_by = 25


class CitiesList(ListView):
    model = Cities
    template_name = "supermarkets/cities_list.html"
    context_object_name = "cities"
    paginate_by = 25


class ReceiveSupermarketsFromQuery(ListView):
    model = Supermarket
    template_name = "supermarkets/market_list.html"
    paginate_by = 25
    context_object_name = "supermarkets"

    def get_queryset(self):
        size = self.kwargs.get('size', None)
        page = self.kwargs.get('page', None)
        search = self.kwargs.get('search', None)
        postcode = self.kwargs.get('postcode', None)

        if search is not None:
            search_split = search.lower().split()

        markets = Supermarket.objects.all()
        
        matches = []
        
        for market in markets:
            market_info = "".join[market.address, market.name, market.city.postcode, market.city.name]
            if any([s in market_info for s in search_split]):
                matches.append(market.id)

        queryset = super().get_queryset()
        
        
        filtered = queryset.filter(pk__in=matches)
        
        # .values('address','id', 'name')
        serialized_q = json.dumps(list(filtered), cls=DjangoJSONEncoder)
        JsonResponse(serialized_q)

        return filtered
    


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







