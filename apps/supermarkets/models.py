import uuid

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.conf import settings


from django.db import transaction
from django.conf import settings


class Supermarket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    city = models.ForeignKey(
        "supermarkets.Cities",
        related_name="supermarkets",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = models.Manager()

    @property
    def waiting_queue_last_hour(self):
        return self.warnings.all().count()



class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    postcode = models.IntegerField(validators=[
        MaxValueValidator(99999),
        MinValueValidator(1001)]
    )
    name = models.CharField(max_length=256)


class Warn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=256, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    supermarket = models.ForeignKey(
        "supermarkets.Supermarket",
        related_name="warnings",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )



#     def accept_warning(self,w,seconds=60*60*3): # eine Warnung in 3 Stunden
#         n = datetime.datetime.now()
#         old_warnings = [ ww for ww in  self.list_of_warnings if w.hashed == ww.hashed]
#         if len(old_warnings)>0:
#             m = min([ww.dtime for ww in old_warnings])
#             M = max([ww.dtime for ww in old_warnings])
#             if (n-M).total_seconds()>seconds:
#                 self.list_of_warnings.append(w)
#                 return True
#             else:
#                 return False
#         else:
#             self.list_of_warnings.append(w)
#             return True
        
    
#     def delete_old_warnings(self,seconds = 60*60):
#         n = datetime.datetime.now()
#         print([str(x) for x in self.list_of_warnings])
#         self.list_of_warnings = [w for w in self.list_of_warnings if (n-w.dtime).total_seconds() <= seconds]


# id = 1
# supermarkets = [Supermarket(1,65549,"Musterstr.",supermarket) for supermarket in supermaerkte]
# for supermarket in  supermarkets:
#     supermarket.id = id
#     id +=1
# supermarkets_by_id = dict([(supermarkt.id,supermarkt) for supermarkt in supermarkets])
# supermarkets_by_postcode = dict([(supermarkt.postcode,supermarkt) for supermarkt in supermarkets])
        
