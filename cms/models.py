from django.db import models


# Create your models here.
class Company(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    name = models.CharField(max_length=25)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Content(models.Model):
    name = models.CharField(max_length=25)
    page_url = models.CharField(max_length=255)
    page_section = models.CharField(max_length=25)
    priority = models.IntegerField()
    status = models.CharField(max_length=15)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    schedules = models.ManyToManyField(Schedule, blank=True)
    content_type = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Piece(models.Model):
    key = models.CharField(max_length=25)
    value = models.TextField(null=True, blank=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    upload = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.key


class Media(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
