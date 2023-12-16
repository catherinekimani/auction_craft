from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . inherit import cartData
# forms
from .forms import BidForm, AuctionItemForm
# messages
from django.contrib import messages

# register
def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            if 'full_name' in request.POST:
                username = request.POST['username']
                full_name = request.POST['full_name']
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                phone_number = request.POST['phone_number']
                email = request.POST['email']

                if password1 != password2:
                    alert = True
                    return render(request, "users/register.html", {'alert': alert})

                user = User.objects.create_user(username=username, password=password1, email=email)
                customers = Customer.objects.create(user=user, name=full_name, phone_number=phone_number, email=email)
                user.save()
                customers.save()

                user = authenticate(request, username=username, password=password1)
                login(request, user)

                return redirect("home")

            else:
                alert = True
                return render(request, "users/register.html", {'alert': alert})
    return render(request, "users/register.html")

# login
def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print("User authenticated successfully.")
                return redirect("/")
            else:
                alert = True
                error_message = "Incorrect username or password. Please try again."
                return render(request, "users/login.html", {"alert": alert, "error_message": error_message})
    return render(request, "users/login.html")

# logout
def Logout(request):
    logout(request)
    alert = True
    return render(request, "users/home.html", {'alert':alert})

# when use is logged in
def loggedin_contact(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method=="POST":       
        name = request.user
        email = request.user.email
        phone = request.user.customer.phone_number
        desc = request.POST['desc']
        contact = UserContact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        alert = True
        return render(request, 'loggedin_contact.html', {'alert':alert})
    return render(request, "users/loggedin_contact.html", {'cartItems':cartItems})

# change password
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "users/change_password.html", {'cartItems':cartItems})

# home page
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Redirect admin users to the admin dashboard
            return redirect('admin:index')

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    products = AuctionItem.objects.all()

    # Fetch highest bid for each product
    for product in products:
        bids = Bid.objects.filter(item=product).order_by('-amount')
        highest_bid = bids.first()
        product.highest_bid = highest_bid

    if request.method == "POST":
        bid_form = BidForm(request.POST)
        auction_item_form = AuctionItemForm(request.POST, request.FILES)

        if bid_form.is_valid():
            pass

        elif auction_item_form.is_valid():
            auction_item = auction_item_form.save(commit=False)
            auction_item.seller = request.user
            auction_item.save()
            messages.success(request, 'Auction item added successfully.')
            return redirect('home')

        else:
            messages.error(request, 'Invalid bid or auction item form.')

    else:
        bid_form = BidForm()
        auction_item_form = AuctionItemForm()

    context = {
        'products': products,
        'cartItems': cartItems,
        'bid_form': bid_form,
        'auction_item_form': auction_item_form,
    }
    return render(request, "users/home.html", context)

# cart page
def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = AuctionItem.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return render(request, "users/cart.html", {'items':items, 'order':order, 'cartItems':cartItems})

# checkout
def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    total = order.get_cart_total
    if request.method == "POST":
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        phone_number = request.POST['phone_number']
        payment = request.POST['payment']
        shipping_adress = PurchaseDetail.objects.create(address=address, city=city, phone_number=phone_number, state=state, zipcode=zipcode, customer=request.user.customer, total_amount=total, order=order, payment=payment)
        shipping_adress.save()
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        id = order.id  
        alert = True
        return render(request, "users/checkout.html", {'alert':alert, 'id':id})
    return render(request, "users/checkout.html", {'items':items, 'order':order, 'cartItems':cartItems})

# item update
def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action:', action)
    print('productID:', productID)

    customer = request.user.customer
    product = AuctionItem.objects.get(id=productID)
    order, created = Purchase.objects.get_or_create(customer=customer, complete=False)

    if product.seller != customer.user:
        orderItem, created = PurchaseItem.objects.get_or_create(order=order, product=product)
        update_order, created = OrderUpdate.objects.get_or_create(order_id=order, desc="Your Order is Successfully Placed.")

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()
        update_order.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        # updated cart data
        data = cartData(request)
        items = data['items']
        order = data['order']
        cartItems = data['cartItems']

        response_data = {
            'message': 'Item was added' if action == 'add' else 'Item was removed',
            'cartItems': cartItems,
            'orderTotal': order.get_cart_total,
        }

        return JsonResponse(response_data, safe=False)

    else:
        return JsonResponse('You cannot add your own item to the cart', safe=False)

# product view
def product_view(request, myid):
    product = AuctionItem.objects.filter(id=myid).first()
    feature = AuctionItemFeature.objects.filter(product=product)
    reviews = AuctionItemReview.objects.filter(product=product)
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    if request.method=="POST":
        customer = request.POST['customer']
        content = request.POST['content']
        review = AuctionItemReview(customer=customer, content=content, product=product)
        review.save()
        return redirect(f"/product_view/{product.id}")
    return render(request, "users/items.html", {'product':product, 'cartItems':cartItems, 'feature':feature, 'reviews':reviews})

# search
def search(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method == "POST":
        search = request.POST['search']
        products = AuctionItem.objects.filter(name__contains=search)
        return render(request, "users/search.html", {'search':search, 'products':products, 'cartItems':cartItems})
    else:
        return render(request, "users/search.html")


# contact
def contact(request):
    if request.method=="POST":       
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        contact = UserContact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        alert = True
        return render(request, 'users/contact.html', {'alert':alert})
    return render(request, "users/contact.html")

# bid view
def place_bid(request, myid):
    item = AuctionItem.objects.get(id=myid)
    highest_bid = Bid.objects.filter(item=item).order_by('-amount').first()

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['amount']

            if highest_bid and bid_amount <= highest_bid.amount:
                messages.error(request, 'Your bid must be higher than the current highest bid.')
            else:
                bid = Bid(customer=request.user.customer, item=item, amount=bid_amount)
                bid.save()
                messages.success(request, 'Bid placed successfully.')
                return redirect('place_bid', myid=item.id)
    else:
        form = BidForm()

    bid_end_time = item.bid_end_time
    return render(request, 'users/place_bid.html', {'form': form, 'item': item, 'highest_bid': highest_bid, 'bid_end_time': bid_end_time})

# user product view
def user_products(request):
    if request.user.is_authenticated:
        user = request.user
        products = AuctionItem.objects.filter(seller=user)
        return render(request, 'users/user_products.html', {'products': products})
    else:
        return render(request, 'not_authenticated.html')
    
# footer
def footer_view(request):
    return render(request, 'users/footer.html')
