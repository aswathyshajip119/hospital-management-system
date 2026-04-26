from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    experience = models.IntegerField()
    op_time = models.CharField(max_length=100, blank=True, null=True)
    available_days = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


