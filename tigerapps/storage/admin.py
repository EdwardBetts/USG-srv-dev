from models import *
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'content', 'visible','posted']})
    ]
    list_display = ('title','posted')
    search_fields = ['title', 'content','posted']

class TimeAdmin(admin.ModelAdmin):
    list_display = ('slot_id', 'n_boxes_total', 'n_boxes_bought',
                    'dropoff_date', 'dropoff_time_start', 'dropoff_time_end',
                    'pickup_date', 'pickup_time_start', 'pickup_time_end')
    
    
class UnpaidOrderAdmin(admin.ModelAdmin):
    #everything but timestamp
    fieldsets = [(None, {'fields': ['user', 'cell_number', 'dropoff_pickup_time',
                                    'proxy_name', 'proxy_email',
                                    'n_boxes_bought', 'invoice_id', 'signature']})]
    list_display = ('user', 'cell_number', 'n_boxes_bought', 'invoice_id', 'timestamp')
    search_fields = ['user__username', 'proxy_name', 'proxy_email']
    
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['user', 'cell_number', 'dropoff_pickup_time',
                                    'proxy_name', 'proxy_email',
                                    'n_boxes_bought', 'invoice_id', 'signature',
                                    'bool_picked_empty', 'n_boxes_dropped', 'n_boxes_picked', 'year']})]
    list_display = ('user', 'cell_number', 'n_boxes_bought',
                    'proxy_name', 'proxy_email', 'dropoff_pickup_time',
                    'bool_picked_empty', 'n_boxes_dropped', 'n_boxes_picked')
    #search_fields = ['user__username', 'proxy_name', 'proxy_email', 'dropoff_pickup_time', 'year']
    search_fields = ['user__username']
    

admin.site.register(Post, PostAdmin)
admin.site.register(DropoffPickupTime, TimeAdmin)
admin.site.register(UnpaidOrder, UnpaidOrderAdmin)
admin.site.register(Order, OrderAdmin)
