from django.shortcuts import redirect, render
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(topic__name__icontains=q))
    topics = Topic.objects.all()
    return render(request, 'base/home.html', {'rooms': rooms, 'topics': topics})

def room(request):
    rooms = Room.objects.all()
    return render(request, 'base/room.html', {'room': rooms})

def room(request, pk):
    rooms = Room.objects.get(id=int(pk))
    return render(request, 'base/room.html', {'room': rooms})

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    context = {'form': form}
    return render(request, 'base/room_form.html', context)  

def updateRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home') 
    context = {'form': form}
    return render(request, 'base/room_form.html', context)  

def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home') 
    return render(request, 'base/delete.html', {'room': room})
