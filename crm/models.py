from django.db import models


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        """display first name and last name in the Django Admin"""
        return (f"{self.first_name} {self.last_name}")


class Event(models.Model):
    name = models.CharField(max_length=200)
    time = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
