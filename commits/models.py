from django.db import models
import uuid
import shortuuid

def conver_encode():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s


class Commit(models.Model):
    id_commit = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    url = models.URLField(null=True)
    sha = models.CharField(max_length=40, null=True)  
    node_id = models.CharField(max_length=100, null=True)
    html_url = models.URLField(null=True)
    comments_url = models.URLField(null=True)
    commit_url = models.URLField(null=True)
    author_name = models.CharField(max_length=100, null=True)
    author_email = models.EmailField(null=True)
    author_date = models.DateTimeField(null=True)
    committer_name = models.CharField(max_length=100, null=True)
    committer_email = models.EmailField(null=True)
    committer_date = models.DateTimeField(null=True)
    message = models.TextField(null=True)
    tree_url = models.URLField(null=True)
    tree_sha = models.CharField(max_length=40, null=True)
    comment_count = models.IntegerField(null=True)
    author_login = models.CharField(max_length=100, null=True)
    author_id = models.IntegerField(null=True)
    author_avatar_url = models.URLField(null=True)
    author_html_url = models.URLField(null=True)
    committer_login = models.CharField(max_length=100, null=True)
    committer_id = models.IntegerField(null=True)
    committer_avatar_url = models.URLField(null=True)
    committer_html_url = models.URLField(null=True)

    def __str__(self):
        return self.id_commit
