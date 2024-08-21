from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
from django.conf import settings
from books.models import Book


# ORDER INFORMATION
class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)     
    
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        self.order_total = self.items.aggregate(Sum('item_total'))['item_total__sum'] 
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_COST / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()
        
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.order_number                 
    
    
# ORDER ITEM INFORMATION
class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False, blank=False, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, editable=False)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.item_total = self.book.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.quantity} of {self.book.title}'
