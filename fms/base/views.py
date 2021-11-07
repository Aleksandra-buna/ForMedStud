from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Пользователь или пароль введены не верно!')

    context = {'page': page}

    return render(request, 'base/login.html', context)


def logout_event(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Пароли не совпадают, попробуйте снова')

    context = {'form': form}

    return render(request, 'base/login.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(name__icontains=q) |
                                Q(topic__name__icontains=q))

    count_rooms = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'count_rooms': count_rooms}

    return render(request, 'base/home.html', context)


def room_page(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all().order_by('-created')

    if request.method == 'POST':
        create_message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'msgs': msgs}

    return render(request, 'base/room_page.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/create_room.html', context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/create_room.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete_room.html', context)
# Create your views here.
