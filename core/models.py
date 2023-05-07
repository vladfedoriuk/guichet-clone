from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        return self.orderitem_set.all()


class OrderItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=1, null=True)
    created = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        total = self.event.price * self.quantity if self.quantity else self.price
        return total
