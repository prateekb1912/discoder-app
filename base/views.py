from django import forms
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import  UserCreationForm

from .models import Message, Room, Topic
from .forms import RoomForm

def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
            print(user)
        except:
            print("ERORO HERE")
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "Invalid username or password")

    context = {"page": page}

    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "An error occured")

    context = {"page": page, "form": form}

    return render(request, "base/login_register.html", context)

def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = query) | 
        Q(name__icontains = query) |
        Q(desc__icontains = query)
    )
 
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_msgs = Message.objects.all()

    context = {
        'rooms':rooms, 
        'topics':topics, 
        'room_count': room_count,
        'room_msgs': room_msgs}
    return render(request, 'base/home.html', context)

def room(request, id):
    room = Room.objects.get(id = id)
    comments = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == 'POST':
        room_msg = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('comment')
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)
    
    context = {
        'room': room, 
        'comments':comments,
        'participants': participants}

    return render(request, 'base/room.html', context)

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def updateRoom(request, id):
    room = Room.objects.get(id = id)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse("You are not allowed HERREEEE!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def deleteRoom(request, id):
    room = Room.objects.get(id = id)

    if request.user != room.host:
        return HttpResponse("You are not allowed HERREEEE!")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url = 'login')
def deleteMessage(request, id):
    msg = Message.objects.get(id = id)

    if request.user != msg.user:
        return HttpResponse("You are not allowed HERREEEE!")
    if request.method == 'POST':
        msg.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': msg})