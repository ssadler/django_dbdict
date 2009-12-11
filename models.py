from django.db import models

class Entry(models.Model):
    name = models.CharField(max_length=255)
    key_hash = models.PositiveIntegerField()
    key = models.CharField(max_length=255)
    data = models.TextField()
    
    class Meta:
        unique_together = (('name', 'key_hash'),)
    
    def __unicode__(self):
        return "%s/%s" % (self.name, self.key)
