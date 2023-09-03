import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


#API routes
@csrf_exempt
@login_required
def compose(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    # Get content of post
    content = data.get("content", "")

    # Create post
    post = Post(
        poster=request.user,
        content=content,
        likes=0
    )
    post.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)

@csrf_exempt
@login_required
def post(request, post_id):

    # Query for requested email
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update the likes or edit
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes = data["likes"]
            
        if data.get("content") is not None:
            post.content = data["content"]
         
        post.save()
        return HttpResponse(status=204)

    # post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

#Functions

#helpers

def isFollowing(online, user):
    if online.userprofile not in user.userprofile.follows.all():
        return False
    else:
        return True

def isFollowingString(online, user):
    if isFollowing(online, user):
        return "Unfollow"
    return "Follow"


def initializePaginator(page_number, posts):
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10) 
    return paginator.get_page(page_number) 


def getPostsFromFollowing(user):
    fs = user.userprofile.followed_by.all()
    follows = [f.user for f in fs]
    return Post.objects.filter(poster__in=follows)


#request functions

def index(request):
    return render(request, "network/index.html", {
        "page_posts": initializePaginator(request.GET.get('page'), Post.objects.all()),
        "title": "All posts"
    })


def following(request):
    posts = getPostsFromFollowing(request.user)
    return render(request, "network/index.html", {
        "page_posts": initializePaginator(request.GET.get('page'), posts),
        "title": "Following"
    })



def profile(request, username):
    try:
        user = User.objects.get(username=username)   
    except User.DoesNotExist:
        return render(request, "network/nopage.html")

    return render(request, "network/index.html", {
        "username": user,
        "followers_count": len(user.userprofile.follows.all()),
        "following_count": len(user.userprofile.followed_by.all()),
        "follow_unfollow": isFollowingString(request.user, user),
        "page_posts": initializePaginator(request.GET.get('page'), Post.objects.filter(poster=user)),  
    })

def follow(request, user_id):
    user = User.objects.get(id=user_id)
    online = request.user
    
    if not isFollowing(online, user):
        user.userprofile.follows.add(online.userprofile)
    else:
        user.userprofile.follows.remove(online.userprofile)

    return HttpResponseRedirect(reverse("profile", args=[user]))
    
        
def new(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse(index))
    return render(request, "network/compose.html")
