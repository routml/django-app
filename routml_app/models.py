from django.db import models

class Url(models.Model):
    url = models.CharField(max_length=2000, unique=True, db_index=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
