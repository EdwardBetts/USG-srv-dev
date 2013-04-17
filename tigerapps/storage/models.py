from django.db import models
from django.contrib.auth.models import User
import datetime

class Post(models.Model):
    title = models.CharField(max_length=40, unique=True, help_text="Title of the Post")
    content = models.TextField(help_text="Actual content, pure HTML")
    posted = models.DateTimeField(default=datetime.datetime.now(), help_text="Date posted")
    visible = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title

class DropoffPickupTime(models.Model):
    '''
    User's selection from possible dropoff and pickup times of an order
    '''
    slot_id = models.CharField("Slot ID", max_length=1)
    dropoff_date = models.DateField("Dropoff date")
    dropoff_time_start = models.TimeField("Dropoff time start")
    dropoff_time_end = models.TimeField("Dropoff time end")
    pickup_date = models.DateField("Pickup date")
    pickup_time_start = models.TimeField("Pickup time start")
    pickup_time_end = models.TimeField("Pickup time end")
    n_boxes_total = models.IntegerField("Total boxes available")
    n_boxes_bought = models.IntegerField("Total boxes bought", default=0)
    year = models.IntegerField(default=2013)

    def __unicode__(self):
        return "%s, Dropoff: %s %s-%s, Pickup: %s %s-%s" % (self.slot_id,
                                                            self.dropoff_date.strftime("%a %m/%d/%Y"),
                                                            self.dropoff_time_start.strftime("%I:%M").lstrip('0'),
                                                            self.dropoff_time_end.strftime("%I:%M%p").lstrip('0'),
                                                            self.pickup_date.strftime("%a %m/%d/%Y"),
                                                            self.pickup_time_start.strftime("%I:%M").lstrip('0'),
                                                            self.pickup_time_end.strftime("%I:%M%p").lstrip('0'))


class UnpaidEmailManager(models.Manager):
    def all(self):
        ordered_users = set(order.user.username for order in Order.objects.all())
        return set(obj.user.username+'@princeton.edu' for obj in self.model.objects.all() if obj.user.username not in ordered_users)

class UnpaidOrder(models.Model):
    '''
    All info describing a student's order; not paid for yet (student can have multiple of these orders)
        User: Name, Email
        Cell phone #
        Proxy name, Proxy email, 
        # Boxes registered for,
    '''
    user = models.ForeignKey(User, related_name="unpaid_order")
    cell_number = models.CharField("Cell phone number", max_length=14)
    dropoff_pickup_time = models.ForeignKey(DropoffPickupTime, verbose_name="Dropoff/pickup times", related_name="unpaid_order")
    proxy_name = models.CharField("Proxy name", max_length=50, blank=True)
    proxy_email = models.CharField("Proxy email", max_length=50, blank=True)
    n_boxes_bought = models.IntegerField("Quantity", max_length=2)
    invoice_id = models.CharField("Invoice ID", max_length=36, unique=True)
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)
    signature = models.CharField("Signature", max_length=50)
    year = models.IntegerField(default=2013)
    
    emails = UnpaidEmailManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.user.username


class PaidEmailManager(models.Manager):
    def all(self):
        return set(obj.user.username+'@princeton.edu' for obj in self.model.objects.all())

class Order(models.Model):
    '''
    All info describing a student's order
        User: Name, Email
        Cell phone #
        Proxy name, Proxy email, 
        # Boxes paid for,
        picked up empty box (Y/N),
        dropoff time, # boxes dropped off, 
        pickup time, # boxes picked up, 
    '''
    
    user = models.ForeignKey(User, related_name="order", unique=False,)
    cell_number = models.CharField("Cell phone number", max_length=14)
    dropoff_pickup_time = models.ForeignKey(DropoffPickupTime, verbose_name="Dropoff/pickup times", related_name="order")
    proxy_name = models.CharField("Proxy name", max_length=50, blank=True)
    proxy_email = models.CharField("Proxy email", max_length=50, blank=True)
    n_boxes_bought = models.IntegerField("Quantity", max_length=2)
    invoice_id = models.CharField("Invoice ID", max_length=36, unique=True)
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)
    signature = models.CharField("Signature", max_length=50)
    year = models.IntegerField(default=2013)
    
    bool_picked_empty = models.BooleanField("Picked up Empty Boxes", default=False)
    n_boxes_dropped = models.IntegerField("# Dropped Off", max_length=2, blank=True, default=0)
    n_boxes_picked = models.IntegerField("# Picked Up", max_length=2, blank=True, default=0)
    
    emails = PaidEmailManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.user.username
