import httpx

from django.shortcuts import redirect, render
from .forms import PostForm
from django.conf import settings


async def index(request):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/users/users/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
        )
        posts_response = await client.get(
            "http://localhost:8000/users/posts/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
        )
    users = response.json()
    posts = posts_response.json()
    print(users)
    print(posts)
    
    return render(request, "users/index.html", {"users": users, "posts": posts})


async def detail(request, id):
    print("ID is ", id)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/users/users/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
        )
    user = response.json()
    print(user)
    return render(request, "users/detail.html", {"user": user})

async def delete_post(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            post_response = await client.delete(
            f"http://localhost:8000/users/posts/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
            )
        return redirect("/users")

    return render(request, "users/delete_post.html")

async def edit_post(request, id):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            post_response = await client.put(
                f"http://localhost:8000/users/posts/{id}/",
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                data=request.POST
            )
        return redirect("/users")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/users/posts/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},)
    post = response.json()
    print(post)

    return render(request, "users/edit_post.html", { "post": PostForm(initial={
        "id": post["id"],
        "title": post["title"],
        "body": post["body"],
    }) })

async def add_post(request):
    if request.method == "POST":
        async with httpx.AsyncClient() as client:
            post_response = await client.post(
                f"http://localhost:8000/users/posts/",
                headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                data=request.POST
            )
        return redirect("/users")

    return render(request, "users/add_post.html", { "post": PostForm()})

