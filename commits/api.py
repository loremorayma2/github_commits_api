import requests
from django.http import JsonResponse
import os
import json
from django.core.cache import cache 
from .models import Commit
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def post_commits(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        owner = data.get('owner')
        repo = data.get('repo')

        if not owner or not repo:
            return JsonResponse({"error": "Missing 'owner' or 'repo' in request data."}, status=400)
        
        if owner!="loremorayma2":
            return JsonResponse({"error": "User not allowed."}, status=400)
        
        if repo!="github_commits_api" or repo!="github_commits":
            return JsonResponse({"error": "Repos not allowed."}, status=400)
        
        cache_key = f'commits-{owner}-{repo}'
        cached_response = cache.get(cache_key)

        if cached_response is not None:
            return JsonResponse(cached_response, safe=False)

        url_root = os.getenv('GITHUB_URL')
        token = os.getenv('GITHUB_ACCESS_TOKEN')
        endpoint = f"{url_root}repos/{owner}/{repo}/commits"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}"
        }
        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code==404:
            return JsonResponse({"error":"Not Found"}, safe=False)
        if response.status_code==500:
            return JsonResponse({"error":"Server error"}, safe=False)
        if response.status_code==400:
            return JsonResponse({"error":"Bad Request "}, safe=False)
        
        if response.status_code == 200:
            commits_data = response.json()
            for commit_data in commits_data:
                sha = commit_data.get('sha')
                commit_info = commit_data.get('commit', {})
                message = commit_info.get('message', '')

                commit, created = Commit.objects.update_or_create(
                    sha=sha,
                    defaults={
                        'message': message,
                        'repo_name': repo 
                    }
                )

            cache.set(cache_key, commits_data, timeout=900)
            return JsonResponse(commits_data, safe=False)
