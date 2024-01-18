import requests
from django.http import JsonResponse
import os
import json
from django.core.cache import cache 
from .models import Commit
from .serializers import CommitSerializer
from rest_framework.decorators import api_view
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from dotenv import load_dotenv
load_dotenv()


def get_access():
    url_root = os.getenv('GITHUB_URL')
    token = os.getenv('GITHUB_ACCESS_TOKEN')
    return url_root,token

def get_repos(url_root,username,token):
    endpoint = f"{url_root}users/{username}/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(endpoint, headers=headers)
    if check_response_errors(response):
        return JsonResponse({'error':'Error de respuesta'},status=response.status_code)
    save_commits(response.json(),username)

def fetch_commits(repo_name, username):
    commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    commits_response = requests.get(commits_url)
    if commits_response.status_code == 200:
        return commits_response.json()
    return None

def save_commits(repos, username):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_repo = {executor.submit(fetch_commits, repo['name'], username): repo for repo in repos}
        new_commits = []
        for future in as_completed(future_to_repo):
            commits = future.result()
            if commits:
                repo_name = future_to_repo[future]['name']
                new_commits.extend(
                    Commit(
                        sha=commit["sha"],
                        author=commit["commit"]["author"]["name"],
                        message=commit["commit"]["message"],
                        repo_name=repo_name
                    )
                    for commit in commits
                )

    existing_shas = set(Commit.objects.filter(
        sha__in=[commit.sha for commit in new_commits]
    ).values_list('sha', flat=True))

    new_commits = [commit for commit in new_commits if commit.sha not in existing_shas]

    with transaction.atomic():
        Commit.objects.bulk_create(new_commits, ignore_conflicts=True)
        

def check_response_errors(response):
    if response.status_code == 200:
        return False
    return True




@api_view(['POST'])
def get_commits(request):

    if not request.method == 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=405)
        
    if not request.data.get('username'):
        return JsonResponse({"error": "Debe enviar el dato username"}, status=400)
    
    if not request.data.get('username')=='loremorayma2':
        return JsonResponse({"error": "Nombre de usuario no permitido"}, status=405)
    
    
    username = request.data.get('username')
    url_root, token = get_access()

    cache_key = f'commits_{username}'
    cache_time = 60 * 15

    cached_data = cache.get(cache_key)

    if cached_data is None:
        repo_response = get_repos(url_root, username, token)
        if isinstance(repo_response, JsonResponse):  
            return repo_response  

        commits = Commit.objects.all().order_by('-created_at')
        serializer = CommitSerializer(commits, many=True)
        cache.set(cache_key, serializer.data, cache_time)
        data_to_return = serializer.data  
    else:
        data_to_return = cached_data  
    
    return JsonResponse(data_to_return, safe=False) 



        