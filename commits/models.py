from django.db import models
import uuid
import shortuuid
from django.utils import timezone

def conver_encode():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s


class Commit(models.Model):
    id_commit = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    sha = models.CharField(max_length=300,null=True) 
    message = models.TextField(null=True) 
    repo_name = models.CharField(max_length=100,null=True)
    author = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.repo_name} - {self.sha} - {self.author}"
    
    class Meta():
        db_table="commit"
