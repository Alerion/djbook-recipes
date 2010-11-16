from django.db import models

class Packet(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
class Channel(models.Model):
    
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='uploads/channels/')
    cost = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name