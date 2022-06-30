from re import I
from django.shortcuts import render,get_object_or_404
from urllib3 import HTTPResponse
from .models import *
from .forms import *
from django.conf import settings
from django.urls import reverse
from .utils import get_plot
# from django.views.generic import LikeView
import json
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response
# Create your views here.
from django.shortcuts import render, redirect
from .models import Category
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from datetime import datetime
import datetime
import calendar
from .decorators import unauthenticated_user, allowed_user, admin_only


#############################------LOGINView-------###########################


@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    return redirect('login')

def logoutUser(request):
    logout(request)
    return redirect('/login/')





def loginpage(request):
    if request.method == "POST" and 'form1' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(5000)
            return redirect('/')
        else:
            messages.error(request, 'INCORRECT USERNAME OR PASSWORD! TRY AGAIN')
    

    form = CreateUserForm()
    if request.method == 'POST' and 'form2' in request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account Created Successfully for ' + username)

    context = {'form': form }

    return render(request, 'login.html', context)

################################------Index-------##########################


# Create your views here.
def index(request):
    now = datetime.datetime.now()
    format = '%H:%M:%S %p'
    current_time = now.strftime(format)
    current_date = now.strftime("%d-%m-%Y")
    cust = Customer.objects.all()
    prod = Product.objects.all()
    cat = Category.objects.all()
    context = {'cc': cat, 'name': cust, 'prod': prod,
               'time': current_time, 'day': current_date}
    return render(request, 'index.html', context)


################################------Profile-------##########################

@login_required(login_url='login')
def userProfile(request):
    cust = Customer.objects.all()
    calenda = calendar.month(2021, 10)
    prod = Product.objects.all()
    customer1 = request.user.customer
    form = CustomerForm(instance=customer1)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer1)
        if form.is_valid():
            form.save()
    context = {'form': form, 'cal': calenda, 'name': cust, 'prod': prod}
    return render(request, 'profile.html', context)

################################------Update-cart-------##########################


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("product", productId)
    print("action", action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    elif action == 'delete':
        orderItem.delete()

    return JsonResponse(('Item was Added'), safe=False)

################################------Cart-------##########################


def analytics(request):
    qs = Product.objects.all()
    x = [x.name for x in qs]
    y = [y.price for y in qs]
    chart = get_plot(x, y)
    context = {'chart': chart}
    return render(request, 'analytics.html', context)


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        Items = order.orderitem_set.all()
        
    else:
        Items = []

    context = {'Items': Items, 'order': order}
    return render(request, 'cart.html', context)


def initiate_payment(request):
    received_data = ''
    Tid = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        orderItems , created  = OrderItem.objects.get_or_create(order=order)
        orderItem = order.orderitem_set.all()
        
    else:
        orderItem = []
        orderItem.save()
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})
    # transaction = OrderItem.objects.create(product=Product)
    # transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(Tid)),
        ('CUST_ID', str(request.user.customer)),
        ('TXN_AMOUNT', str(order.get_cart_total)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        ##('EMAIL', request.user.email),
        ##('MOBILE_N0', '8652012693'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksums = generate_checksum(paytm_params, merchant_key)
    is_verify = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY,checksums)
    print(is_verify)
    order.checksum = checksums  
    order.transaction_id = checksums+'Product_DONE'
    order.save()
    paytm_params['CHECKSUMHASH'] = checksums
    # report = Transaction.objects.get(Order =str(Tid))
    # print(report)
    print('SENT: ', checksums)
    order.save()
    if is_verify:
        orderItems.transaction_id = checksums
        orderItems.checksum = checksums+str(Tid)
        orderItems.save()

    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
    paytm_params = {}
    paytm_checksum = received_data['CHECKSUMHASH'][0]
    for key, value in received_data.items():
        if key == 'CHECKSUMHASH':
            paytm_checksum = value[0]
        else:
            paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            
        else:
            received_data['message'] = "Checksum Mismatched"
            obj = OrderItem.objects.filter(status="Pending").update(status = 'OnTheWay')
            b = received_data['CHECKSUMHASH']
            print(b)
            
            
            Transaction_report = Transaction.objects.create(
                Order =     received_data['ORDERID'],
                TXN =       received_data['TXNID'],
                Bank_TXN =  received_data['BANKTXNID'],
                Amount =  received_data['TXNAMOUNT'],
                Currency = received_data['CURRENCY'],
                Status = received_data['STATUS'],
                RESPCODE = received_data['RESPCODE'],
                RESPMSG = received_data['RESPMSG'],
                TXN_DATE = received_data['TXNDATE'],
                GATEWAYNAME = received_data['GATEWAYNAME'],
                BANKNAME = received_data['BANKNAME'],
                PAYMENTMODE = received_data['PAYMENTMODE'],
                CHECKSUMHASH = received_data['CHECKSUMHASH'],
                

            )
            Transaction_report.save()
            
            return render(request, 'callback.html', context=received_data)
    else:
        context = received_data
        paytm_params = dict(received_data)
        
    return render(request, 'callback.html', context)

@csrf_exempt
def handlerequest(request):
    merchant_key = settings.PAYTM_SECRET_KEY
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] =form[i]
        if i =='CHECKSUMHASH':
            checksum = form[i]

    verify = verify_checksum(response_dict,merchant_key,checksum)
    if verify:
        if response_dict['RESPCODE'] =='01':
            print('Order Successful')
        else:
            print('Order was not Succesful Because'+response_dict['RESPMSG'])
    context = {'response': response_dict}
    return render(request, 'callback.html',context)
















def home(request):
    context = {}
    return render(request, 'home.html', context)


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/room/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    # profile = request.POST['profile']
    username = request.user.customer
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id,)
    new_message.save()
    return HttpResponse('Message sent successfully')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})


@login_required(login_url='login')
def dashboard(request):
    now = datetime.datetime.now()
    format = '%H:%M:%S %p'
    current_time = now.strftime(format)
    current_date = now.strftime("%d-%m-%Y")
    qs = Product.objects.all()
    x = [x.name for x in qs]
    y = [y.price for y in qs]
    chart = get_plot(x, y)
    cust = Customer.objects.all()
    prod = Product.objects.all()
    cat = Category.objects.all()
    ord = OrderItem.objects.all()
    context = {'cc': cat, 'name': cust, 'prod': prod,'ord':ord,
               'time': current_time, 'day': current_date,'chart': chart}
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def posts(request):
    if request.method == "POST" and 'upload' in request.POST:
        img_name = 'img_name' in request.POST and request.POST['img_name']
        img = 'img' in request.FILES and request.FILES['img']
        u_profile = 'u_profile' in request.POST and request.POST['u_profile']

        img_uploader = Image_Post(image_name=img_name,
                                  image=img,
                                  user=request.user,
                                  user_profile=u_profile,
                                  date=datetime.datetime.now())
        img_uploader.save()
        messages.success(request, 'Your Image Uploaded Successfully !!')
    images = Image_Post.objects.all()

    return render(request, 'SocialMedia.html', {'images': images})


def user_profile(request, user):

    users = User.objects.get(username=user)
    image = Image_Post.objects.filter(user=user)
    prof=Profile.objects.all()

    if request.method == 'POST':
        value=request.POST['value']
        user_follow=request.POST['user']
        follower = request.POST['follower']
        if value == 'follow':
            follower_cnt = Follower_count.objects.create(follower=follower,user=user_follow)
            follower_cnt.save()
            return redirect('/profile/')



    return render(request, 'user-profile.html', {'prof': prof,'users': users, 'image': image})


@login_required
def profile(request):

    if request.method == "POST":
        u_form = UpdateUserForm(instance=request.user, data=request.POST)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')

    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'SM-profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required(login_url='login')
def LikeView(request):
    user = request.user
    if request.method == 'POST':
       prod_id =request.POST.get('prod_id')
       prod_obj = Product.objects.get(id=prod_id)
       if user in prod_obj.liked.all():
           prod_obj.liked.remove(user)
       else:
            prod_obj.liked.add(user)
            
            
       like , created= Likes.objects.get_or_create(user=user,product_likes_id=prod_id)
       
       if not created:
            if like.values=='Like':
                like.values='Unlike'
            else:
                like.values='Like'
       like.save()

    return redirect('home')

def order_status(request):
    orderItemr =  OrderItem.objects.filter(status = 'OnTheWay')
    context = {'orderItemr':orderItemr,}
    return render (request, 'order_status.html',context)