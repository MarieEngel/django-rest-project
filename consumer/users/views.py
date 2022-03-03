import httpx

from django.shortcuts import render
from django.http import HttpResponse


async def index(request):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/users/users/", auth=("admin", "password")
        )
        posts_response = await client.get(
            "http://localhost:8000/users/posts/", auth=("admin", "password")
        )
    users = response.json()
    posts = posts_response.json()
    print(users)
    return render(request, "users/index.html", {"users": users, "posts": posts})


async def detail(request, id):
    print("ID is ", id)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/users/users/{id}/", auth=("admin", "password")
        )
    user = response.json()
    print(user)
    return render(request, "users/detail.html", {"user": user})
