from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=30)
    content_body = models.TextField()
    time = models.DateTimeField()
    version = models.IntegerField(default=0)

    @classmethod
    def exists(cls, id):
        return len(cls.objects.filter(id=id)) > 0