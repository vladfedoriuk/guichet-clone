from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Event, Category, Order, OrderItem


def home(request):
    events = Event.objects.order_by('-date')[:5]
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
        category = get_object_or_404(Category, name=category)
        events = events.filter(category=category)

    context = {
        'events': events
    }
    return render(request, 'core/home.html', context)


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


@login_required
def click_jach(request):
    """
    create order and redirect to cart
    """
    if request.method=='POST':
        event_id=request.POST.get('event_id')
        event=get_object_or_404(Event, pk=event_id)
        # create order with auth user
        order, created = Order.objects.get_or_create(customer=request.user)
        orderitem, created = OrderItem.objects.get_or_create(order=order, event=event, price=event.price)
        if not created:
            orderitem.quantity = orderitem.quantity+1
            orderitem.save()
    # pass the order as the context variable
    order = get_object_or_404(Order, customer=request.user)
    return render(request, 'core/buy_ticket.html', {'order':order})


@login_required
def click_remove(request):
    """
    delete orderitem
    """
    if request.method=='POST':
        orderitem_id=request.POST.get('orderitem_id')
        orderitem=get_object_or_404(OrderItem, pk=orderitem_id)
        orderitem.delete()
    return redirect('order')


@login_required
def quantite(request):
    """
    Add or remove one item
    """
    if request.method=='POST':
        orderitem_id=request.POST.get('orderitem_id')
        orderitem=get_object_or_404(OrderItem, pk=orderitem_id)
        add=request.POST.get('add')
        remove=request.POST.get('remove')
        if add:
            orderitem.quantity = orderitem.quantity + 1
            orderitem.save()
        elif remove:
            if orderitem.quantity == 1:
                orderitem.delete()
            else:
                orderitem.quantity = orderitem.quantity - 1
                orderitem.save()

    return redirect('order')


@login_required
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


@login_required
def profile(request):
    user=request.user
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        if first_name:
            user.first_name=first_name
        if last_name:
            user.last_name=last_name
        if email:
            user.email=email
        user.save()

    return render(request, 'core/profile.html', {'user':user})

