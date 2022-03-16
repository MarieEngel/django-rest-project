import httpx

from django.shortcuts import redirect, render
from .forms import PostForm
from django.conf import settings
from django.core.cache import cache


async def get_content(content):
    result = await cache.aget(content)

    if not result:
        print(content, " not in cache \n")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:8000/users/{content}/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                )
            result = response.json()
            await cache.aset(content, result, 15)

        except httpx.RequestError as exc:
            result = []
    else:
        print(content, " read from cache \n")
    return result


async def index(request):
    context = {"users": [], "posts": [], "uploads": []}
    users = await get_content("users")
    posts = await get_content("posts")
    uploads = await get_content("uploads")

    context["users"] =  users['results']
    context["posts"] =  posts['results']
    context["uploads"] = uploads

    return render(request, "users/index.html", context)


async def detail(request, id):
    context = {"user": None, "connection_error": False}
    print("ID is ", id)
    context["user"] = await cache.aget("user" + id)
    
    if not context["user"]: 
        print("user" + id, " not in cache \n")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:8000/users/users/{id}/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                )
            context["user"] = response.json()
            await cache.aset("user" + id, context["user"], 150)
        except httpx.RequestError as exc:
            context["connection_error"] = True
    else:
        print("user" + id, " read from cache \n")
    print(context)
    print(context["user"])
    return render(request, "users/detail.html", context)


async def delete_post(request, id):
    if request.method == "POST":
        try:
            async with httpx.AsyncClient() as client:
                post_response = await client.delete(
                    f"http://localhost:8000/users/posts/{id}/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
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
                    data=request.POST,
                )
            return redirect("/users")
        except httpx.RequestError as exc:
            return render(request, "users/provider_failed.html")
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:8000/users/posts/{id}/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                )
            post = response.json()
            print(post)

            return render(
                request,
                "users/edit_post.html",
                {
                    "post": PostForm(
                        initial={
                            "id": post["id"],
                            "title": post["title"],
                            "body": post["body"],
                        }
                    )
                },
            )
        except httpx.RequestError as exc:
            return render(request, "users/provider_failed.html")


async def add_post(request):
    if request.method == "POST":
        try:
            async with httpx.AsyncClient() as client:
                post_response = await client.post(
                    f"http://localhost:8000/users/posts/",
                    headers={"Authorization": f"Token {settings.AUTH_TOKEN}"},
                    data=request.POST,
                )
            return redirect("/users")
        except httpx.RequestError as exc:
            return render(request, "users/provider_failed.html")
    return render(request, "users/add_post.html", {"post": PostForm()})
