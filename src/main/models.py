from django.db import models
from accounts.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def store_record(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
class Version(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return self.name

class Task(models.Model):
    NEW = 1
    RESOLVED = 2
    ASSIGNED = 3
    ACCEPTED = 4
    STATUS_CHOICES = (
        (NEW, 'New'),
        (RESOLVED, 'Resolved'),
        (ASSIGNED, 'Assigned'),
        (ACCEPTED, 'Accepted')
    )
    
    BLOCKER = 1
    CRITICAL = 2
    MAJOR = 3
    MINOR = 4
    TRIVIAL = 5
    PRIORITY_CHOICES = (
        (BLOCKER, 'Blocker'),
        (CRITICAL, 'Critical'),
        (MAJOR, 'Major'),
        (MINOR, 'Minor'),
        (TRIVIAL, 'Trivial')
    )
    
    FIXED = 1
    INVALID = 2
    WONTFIX = 3
    DUPLICATE = 4
    WORKSOMEFORM = 5
    RESOLVED_STATUS_CHOICES = (
        (FIXED, 'Fixed'),
        (INVALID, 'Invalid'),
        (WONTFIX, 'Wontfix'),
        (DUPLICATE, 'Duplicate'),
        (WORKSOMEFORM, 'Worksomeform')
    )
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=NEW)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=MAJOR)
    version = models.ForeignKey(Version, null=True, blank=True)
    resolved_status = models.PositiveIntegerField(choices=RESOLVED_STATUS_CHOICES, null=True, blank=True)
    accepted_by = models.ForeignKey(User, related_name='accepted_tasks')
    added_by = models.ForeignKey(User, related_name='created_tasks')
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __unicode__(self):
        return self.name
    
class Comment(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.text[:50]