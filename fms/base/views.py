from django.db import transaction
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Room, Topic, Message, Profile
from .forms import RoomForm, UserForm, MyUserCreationForm, ProfileForm


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
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Данные введены некорректно, пожалуйста попробуйте снова.')

    context = {'form': form}

    return render(request, 'base/login.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(name__icontains=q) |
                                Q(topic__name__icontains=q))
    msgs = Message.objects.filter(Q(room__topic__name__icontains=q))

    count_rooms = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'count_rooms': count_rooms, 'msgs': msgs}

    return render(request, 'base/home.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    # show all user rooms
    rooms = user.room_set.all()
    msgs = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'msgs': msgs, 'topics': topics}

    return render(request, 'base/profile_page.html', context)


@login_required(login_url='login')
@transaction.atomic
def update_user(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile', pk=request.user.id)
        else:
            messages.error(request, 'Некорректный ввод!')

    context = {'user_form': user_form, 'profile_form': profile_form}

    return render(request, 'base/update_profile.html', context)


def room_page(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        create_message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'msgs': msgs, 'participants': participants}

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


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}

    return render(request, 'base/delete_room.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk)
    message.delete()

    return redirect(request.META['HTTP_REFERER'])

# Create your views here.
