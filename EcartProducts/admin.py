from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(FilesAdmin)
admin.site.register(Photo)
admin.site.register(Status)
admin.site.register(Refund)
admin.site.register(Transaction)
admin.site.register(OrderItem) 
# admin.site.register(Likes) 
admin.site.register(Follower_count) 
# admin.site.register(Profile)
# admin.site.register(Image_Post)
# admin.site.register(Order)




@admin.register(Product)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','price','category','num_likes']
    search_fields = ['name','price','category']


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['user','image']


@admin.register(Image_Post)
class Image_Post_Admin(admin.ModelAdmin):
    list_display = ['image_name','user','date']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','get_cart_total','get_cart_items']


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['product','status','quantity','order']


@admin.register(Likes)
class Likes(admin.ModelAdmin):
    list_display = ['id','user','product_likes','values']


admin.site.index_title = 'E-Cart'
admin.site.site_header = 'E-Cart'
admin.site.site_title = 'Welcome TO E-Cart'