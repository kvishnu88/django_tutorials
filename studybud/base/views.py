from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
    

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to the home page if the user is already logged in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Username or password is incorrect')        
            
    return render(request, 'base/login_register.html')

def logoutUser(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


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

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    context = {'form': form}
    return render(request, 'base/room_form.html', context)  

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home') 
    context = {'form': form}
    return render(request, 'base/room_form.html', context)  
    
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home') 
    return render(request, 'base/delete.html', {'room': room})
