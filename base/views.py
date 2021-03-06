from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import  UserCreationForm

from .models import Message, Room, Topic, User
from .forms import RoomForm, UserForm, NewUserCreationForm

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
    form = NewUserCreationForm()

    if request.method == "POST":
        form = NewUserCreationForm(request.POST, request.FILES)
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
 
    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    room_msgs = Message.objects.filter(Q(room__topic__name__icontains=query))

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
def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_msgs = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user, 
        'rooms': rooms, 
        'room_msgs': room_msgs, 
        'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic =  topic,
            name = request.POST.get('name'),
            desc = request.POST.get('desc') 
        )
        
        return redirect('home')
        
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def updateRoom(request, id):
    room = Room.objects.get(id = id)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed HERREEEE!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.desc = request.POST.get('desc')
        
        room.save()
        return redirect('home')

    context = {'room':room, 'form' : form, 'topics': topics}
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


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    context = {
        'form': form
    }

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid:
            form.save()
            return redirect('user-profile', id = user.id)
    return render(request, 'base/update-user.html', context)

def topicsPage(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=query)

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    comments = Message.objects.all()

    context = {
        'comments': comments
    }
    return render(request, 'base/activity.html', context=context)