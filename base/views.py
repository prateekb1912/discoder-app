from django.shortcuts import render

rooms = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Java'},
    {'id': 3, 'name': 'Node.JS'}
]

def home(request):
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, id):
    room = None
    for i in rooms:
        if i['id'] == int(id):
            room  = i

    context = {'room': room}
    return render(request, 'base/room.html', context)