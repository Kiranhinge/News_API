from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SearchResult(models.Model):
    keyword = models.CharField(max_length=255)
    user  =models.ForeignKey(User,  on_delete=models.CASCADE)
    result_title = models.CharField(max_length=255,null=True)
    result_url = models.URLField(null=True)
    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.result_title