from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Event


def home(request):
    events = Event.objects.order_by('-date')[:3]
    context = {
        'events': events
    }
    return render(request, 'core/home.html', context)


def event_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    events = Event.objects.all()

    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        events = events.filter(category=category)

    context = {
        'events': events
    }
    return render(request, 'core/event_list.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event
    }
    return render(request, 'core/event_detail.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    else:
        return render(request, 'core/login.html')


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def buy_ticket(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        # Process the payment and send confirmation email
        messages.success(request, 'Your ticket has been purchased!')
        return redirect('event_detail', event_id=event.id)
    else:
        context = {
            'event': event
        }
        return render(request, 'core/templates/buy_ticket.html', context)
