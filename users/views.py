from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileUpdateForm,ProfileForm, AddToCartForm
from .models import Profile, AuctionItem
# Create your views here.
def home(request):
    best_selling_items = AuctionItem.objects.all()
    return render(request, 'users/home.html', {'best_selling_items': best_selling_items})

def footer_view(request):
    return render(request, 'users/footer.html')

def clients_view(request):
    return render(request, 'users/clients.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}

    return render(request, 'users/register.html', context)

def profile(request):
    current_user = request.user
    
    profile = Profile.objects.filter(user_id = current_user.id).first()
    
    return render(request,'users/profile/profile.html',{"profile":profile})

def editprofile(request):
    
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=request.user)
        
        form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if form.is_valid() and form.is_valid():
            
            form.save()
            
            form.save()
            
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
        form = ProfileUpdateForm(instance=request.user.profile)
        
    return render(request,'users/profile/edit.html',{'form':form})

def add_to_cart(request, item_id):
    item = AuctionItem.objects.get(pk=item_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            total = quantity * item.price

            cart = request.session.get('cart', {})
            cart[item_id] = cart.get(item_id, 0) + quantity
            request.session['cart'] = cart

            return render(request, 'users/cart.html', {'item': item, 'quantity': quantity, 'total': total})
    else:
        form = AddToCartForm()

    return render(request, 'users/add_to_cart.html', {'item': item, 'form': form})
def cart(request):
    cart = request.session.get('cart', {})


    return render(request, 'users/cart.html', {'cart': cart})