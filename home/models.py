from django.db import models

# Create your models here.
# Create your models here.
class SiteHits(models.Model):
    """
    Model to store visitor count 

    """
    visitors = models.CharField(max_length=254, default='visitor')
    count = models.IntegerField(default=0)
