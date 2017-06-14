from django.db import models

# Create your models here.

class Woeid(models.Model):
	name = models.CharField(db_index=True,max_length=32)
