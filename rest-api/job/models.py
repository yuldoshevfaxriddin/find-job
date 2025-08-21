from django.db import models

# Create your models here.

class Job(models.Model):
    name = models.CharField(max_length=200)
    data_offset = models.CharField(null=True, blank=True)
    company_sity = models.CharField(max_length=100, null=True, blank=True)
    company_salary = models.CharField(max_length=100, null=True, blank=True)
    company_image = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    # scraped_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name   