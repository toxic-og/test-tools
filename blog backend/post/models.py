from django.db import models
from user.models import User
# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'post'
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=48, null=False)
    postdate = models.DateTimeField(null=False)

    author = models.ForeignKey(User)

    def __repr__(self):
        return '<{},{},{}>'.format(self.id, self.title, self.postdate)

    __str__ = __repr__

class Content(models.Model):
    class Meta:
        db_table = 'content'
    post = models.OneToOneField(Post)
    content = models.TextField(null=False)
    def __repr__(self):
        return '<{},{},{}>'.format(self.post.id, self.pk, self.content[:10])

    __str__ = __repr__