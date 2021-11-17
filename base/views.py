from django.shortcuts import render

rooms = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Java'},
    {'id': 3, 'name': 'Node.JS'}
]

def home(request):
    context = {'rooms':rooms}
    return render(request, 'home.html', context)

def room(request):
    return render(request, 'room.html')