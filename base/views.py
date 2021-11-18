from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

def home(request):

    query = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(topic__name__icontains = query)
 
    topics = Topic.objects.all()

    context = {'rooms':rooms, 'topics':topics}
    return render(request, 'base/home.html', context)

def room(request, id):
    room = Room.objects.get(id = id)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, id):
    room = Room.objects.get(id = id)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, id):
    room = Room.objects.get(id = id)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})