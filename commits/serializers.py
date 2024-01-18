from rest_framework import serializers
from .models import Commit  # Adjust the import according to your project structure

class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ['sha', 'message', 'repo_name']  # Add all the fields you want to include in the serialization
