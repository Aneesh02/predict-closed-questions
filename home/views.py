from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from home.models import Project, Sentence
import random

# Wikipedia API
import wikipedia

# sentence segmentation
import pysbd


# Create your views here.
def landing(request):
    return render(request, "landing.html")


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("inputPassword")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context = {"error_message": "User does not exist"}
            return render(request, "404.html", context)
    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("/landing")


def registerUser(request):
    if request.method == "POST":
        username = request.POST.get("inputUsername")
        password = request.POST.get("inputPassword")
        if User.objects.filter(username=username).first():
            context = {"error_message": "User already exists"}
            return render(request, "404.html", context)
        else:
            user = User.objects.create_user(username, "", password)
            user.save()
            return redirect("/login")
    else:
        return render(request, "register.html")


def home(request):
    user = request.user
    if user.is_anonymous:
        return redirect("/landing")

    return render(request, "home.html")


def process(request):
    return render(request, "404.html")


def dashboard(request):
    user = request.user

    if request.method == "POST":
        link = request.POST.get("link")
        language = request.POST.get("language")
        number = Project.objects.filter(user=user).count()
        number += 1
        project = Project.objects.create(
            user=user, number=number, link=link, language=language
        )
        project.save()

        try:
            text = wikipedia.summary(link)
        except wikipedia.exceptions.DisambiguationError as e:
            s = random.choice(e.options)
            text = wikipedia.summary(s)

        seg = pysbd.Segmenter(language="en", clean=False)
        sentence_list = seg.segment(text)
        for sline in sentence_list:
            sent_id = Project.objects.filter(user=user).count()
            sent_id += 1
            sentence = sentence.objects.create(
                user=user,
                number=project,
                sentence_id=sent_id,
                original=sline,
                translated="",
            )
            sentence.save()

    projects = Project.objects.filter(user=user)
    context = {"projects": projects}
    return render(request, "dashboard.html", context)


def viewProject(request, pk):
    project = Project.objects.get(id=pk)
    sentences = Sentence.objects.filter(number=project)
    return render(request, "project.html", {"project": project, "sentences": sentences})
