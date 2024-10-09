from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patronage(models.Model):
    title = models.CharField(max_length=30, null=False, unique=True)
    description = models.TextField(null=False)
    img = models.CharField(max_length=80)
    img_background = models.CharField(max_length=80)
    deleted = models.BooleanField()
    class Meta:
        managed = True
        db_table = 'Patronage'

class Disabilities(models.Model):
    STATUS_CHOICES = [
        ('draft','Draft'),
        ('deleted','Deleted'),
        ('formed', 'Formes'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    status = models.CharField(max_length=20, null=False, choices=STATUS_CHOICES)
    data_created = models.DateField(null=False)
    data_compilation = models.DateTimeField()
    data_finished = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests', null=False)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderator_requests')
    class Meta:
        managed = True
        db_table = 'Disabilities'

class Disabilities_Patronage(models.Model):
    disabilities_id = models.ForeignKey(Disabilities, on_delete=models.CASCADE)
    patronage_id = models.ForeignKey(Patronage, on_delete=models.CASCADE)
    comment = models.TextField()
    class Meta:
        managed = True
        db_table = 'Disabilities_Patronage'
    