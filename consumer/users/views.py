import httpx

from django.shortcuts import redirect, render
from .forms import PostForm
from django.conf import settings


async def index(request):
    context = {
        "users": [],
        "posts": [],
        "uploads":[],
        "connection_error": False
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/users/users/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
            )
            posts_response = await client.get(
                "http://localhost:8000/users/posts/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
            )
            uploads_response = await client.get(
                "http://localhost:8000/users/uploads/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
            )
        users = response.json()
        posts = posts_response.json()
        uploads = uploads_response.json()
        print(uploads)
        context["users"] = users["results"]
        context["posts"] = posts["results"]
        context["uploads"] = uploads
    except httpx.RequestError as exc:
        context["connection_error"] = True
    return render(request, "users/index.html", context)


async def detail(request, id):
    context = {
        "user": None,
        "connection_error": False
    }
    print("ID is ", id)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:8000/users/users/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
            )
        user = response.json()
        print(user)
    except httpx.RequestError as exc:
        context["connection_error"] = True
    return render(request, "users/detail.html", context)

async def delete_post(request, id):
    if request.method == "POST":
        try:
            async with httpx.AsyncClient() as client:
                post_response = await client.delete(
                f"http://localhost:8000/users/posts/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                )
            return redirect("/users")
        except httpx.RequestError as exc:
            return render(request, "users/provider_failed.html")

    return render(request, "users/delete_post.html")

async def edit_post(request, id):
    if request.method == "POST":
        try:
            async with httpx.AsyncClient() as client:
                post_response = await client.put(
                    f"http://localhost:8000/users/posts/{id}/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                    data=request.POST
                )
            return redirect("/users")
        except httpx.RequestError as exc:
            return render(request, "users/provider_failed.html")
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://localhost:8000/users/posts/{id}/", headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},)
            post = response.json()
            print(post)
        
            return render(request, "users/edit_post.html", { "post": PostForm(initial={
                "id": post["id"],
                "title": post["title"],
                "body": post["body"],
            }) })
        except httpx.RequestError as exc:
            return render(request, "users/provider_failed.html")

async def add_post(request):
    if request.method == "POST":
        try:
            async with httpx.AsyncClient() as client:
                post_response = await client.post(
                    f"http://localhost:8000/users/posts/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                    data=request.POST
                )
            return redirect("/users")
        except httpx.RequestError as exc:
            return render(request, "users/provider_failed.html")
    return render(request, "users/add_post.html", { "post": PostForm()})

