from datetime import datetime
from secrets import choice
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

from django_countries.data import COUNTRIES



######################------Category------############################
class Category(models.Model):
    name = models.CharField(max_length=2000)
    desc = models.CharField(max_length=2000)

    def __str__(self):
        return self.name



######################---Product---############################

class Product(models.Model):
    name=models.CharField(max_length=255)
    price=models.IntegerField()
    multiple_image = models.FileField(blank=True,null=True)
    image_url=models.CharField(null=True,max_length=2050, default ='' , blank=True)
    description=models.TextField(max_length=1000)
    category=models.ForeignKey(Category,on_delete=CASCADE, max_length=50,null=True)
    image=models.ImageField(null=True,blank=True)
    liked = models.ManyToManyField(User,related_name='blog' ,blank=True)

    def get_image(self):
        if self.image: 
            return self.image.url
        else:
            return ''
          

    def __str__(self):
        return self.name

    @property
    def num_likes(self):
        return self.liked.all().count()


######################---Customer---############################
state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=CASCADE,null=True)
    firstname=models.CharField(max_length=50)
    Image = models.ImageField(default="profile.png",blank=True,null=True)
    lastname=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
        default='Address line 1'
    )

    address2 = models.CharField(
        "Address line 2",
        default='Address line 2',
        max_length=1024,
    )

    pincode = models.IntegerField(null=True
    )

    city = models.CharField(
        "City",
        max_length=1024,
        default='City',
    )

    state = models.CharField(
        "State",
        max_length=1024,
        choices = state_choices,
        default="Maharashtra"
    )

    country = models.CharField(
        "Country",
        max_length=3,
        choices=sorted(COUNTRIES.items()),
        default="IN"
    )
    # uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    
    def __str__(self):
        return self.firstname



class Status(models.Model):
    status=models.CharField(max_length=255,default='')
    type=models.CharField(null=True, max_length=255,default='')
    def __str__(self):
        return self.status




# Create your models here.

class Photo(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    images = models.ImageField(null=False,blank=False)
    desc = models.CharField(max_length=255, null=False,blank=False)
    def __str__(self):
        return self.category.name

######################---Chat_Room---############################

class Room(models.Model):
    name = models.CharField(max_length=10000)
    def __str__(self):
        return self.name

class Message(models.Model):
    value =models.CharField(max_length=1000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    user= models.CharField(max_length=100000)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    room = models.CharField(max_length=1000000)   
    def __str__(self):
        return self.value


######################---File_upload---############################
class FilesAdmin(models.Model):
    upload = models.FileField(upload_to='media')
    Title = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.Title




###########################--------Order---###################################

class Order(models.Model):
    STATUSES = (
    ('Pending', 'Pending'),
    ('Complete', 'Complete'),
    ('OnTheWay', 'On the way'),
    ('Failed', 'Failed'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
)
    status=models.CharField(choices = STATUSES,null=True,max_length=100,default='Pending')   
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True,null=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    # VISTAid = models.CharField(max_length=100, null=True, blank=True)
    transaction_id=models.CharField(max_length=500,null=True,blank=True)
    checksum = models.CharField(max_length=1000, null=True, blank=True)
    # Get_on=models.DateField()
    def __str__(self):
        return f"Id:{self.id},Customer:{self.customer},Status:{self.status}"
        
    def save(self, *args, **kwargs):
        if self.transaction_id is None and self.date_ordered and self.id:
            self.transaction_id = self.date_ordered.strftime('PAY2ME%Y%m%dODR') + str(self.id)+self.checksum
        return super().save(*args, **kwargs)  

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.get_total for items in orderitems])
        return total 
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.quantity for items in orderitems])
        return total 

###########################--------OrderItem---###################################
class OrderItem(models.Model):
    STATUSES = (
    ('Pending', 'Pending'),
    ('Complete', 'Complete'),
    ('OnTheWay', 'On the way'),
    ('Failed', 'Failed'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
)
    status=models.CharField(choices = STATUSES,null=True,max_length=100,default='Pending')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=500,null=True,blank=True)
    checksum = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return f"Id:{self.id},Customer:{self.order.customer},Status:{self.status}"




    @property 
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class Image_Post(models.Model):
    image_name = models.CharField(max_length=100)
    image = models.ImageField(null=True,blank=True)
    user = models.CharField(max_length=100) 
    user_profile = models.CharField(max_length=100)
    date = models.DateField()


state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

class Transaction(models.Model):
    Order = models.CharField(max_length=500,null=True,blank=True)
    TXN = models.CharField(max_length=500,null=True,blank=True)
    Bank_TXN = models.CharField(max_length=500,null=True,blank=True)
    Amount = models.CharField(max_length=500,null=True,blank=True)
    Currency = models.CharField(max_length=500,null=True,blank=True)
    Status = models.CharField(max_length=500,null=True,blank=True)
    RESPCODE = models.CharField(max_length=500,null=True,blank=True)
    RESPMSG =  models.CharField(max_length=500,null=True,blank=True)
    TXN_DATE = models.CharField(max_length=500,null=True,blank=True)
    GATEWAYNAME =models.CharField(max_length=500,null=True,blank=True)
    BANKNAME = models.CharField(max_length=500,null=True,blank=True)
    PAYMENTMODE = models.CharField(max_length=500,null=True,blank=True)
    CHECKSUMHASH = models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return f"Id:{self.Order},Transaction:{self.TXN},Status:{self.Status} of amount {self.Amount}"



class Profile(models.Model):
    name=   models.CharField(max_length=100,blank=True)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    
    def __str__(self):
        return f"Profile of {self.user.username}"


class Follower_count(models.Model):
    follower=models.CharField(max_length=1000)
    user=models.CharField(max_length=1000)
    def __str__(self):
        return str(self.user)

class Likes(models.Model):
    LIKE_Choice = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    product_likes =  models.ForeignKey(Product, on_delete=models.CASCADE,)
    values =  models.CharField(choices=LIKE_Choice, default='Like' ,max_length=100)
    def __str__(self):
        return str(self.product_likes)



class Refund(models.Model):
    REASONS = (
    ('Defect', 'Defect'),
    ('Wrong_Product', 'Wrong Product'),
    ('Not_Delivered_But_Paid', 'Not Delivered But Paid'),
    ('Not_Delivered_on_Time', 'Not Delivered on Time'),
    
)   
    order_refund = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    Reason = models.CharField(choices = REASONS,null=True,max_length=100)
    Feedback = models.TextField(null=True , blank=True)