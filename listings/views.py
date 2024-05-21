from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PropertyForm
from .models import Property
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    print("Register view called")  # Debug statement
    if request.method == 'POST':
        print("POST request received")  # Debug statement
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug statement
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, f'Your account has been created! You are now logged in as {user.username}.')
            return redirect('property_list')
        else:
            print("Form is invalid")  # Debug statement
            print(form.errors)  # Print form errors to the console for debugging
    else:
        print("GET request received")  # Debug statement
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.seller = request.user
            property.save()
            return redirect('my_properties')
    else:
        form = PropertyForm()
    return render(request, 'property_form.html', {'form': form})

@login_required
def my_properties(request):
    properties = Property.objects.filter(seller=request.user)
    return render(request, 'my_properties.html', {'properties': properties})

@login_required
def property_update(request, pk):
    property = Property.objects.get(pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('my_properties')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'property_form.html', {'form': form})

@login_required
def property_delete(request, pk):
    property = Property.objects.get(pk=pk)
    property.delete()
    return redirect('my_properties')



def property_list(request):
    # Apply filters based on request parameters
    city_max = request.GET.get('city_max')
    if city_max:
        properties = properties.filter(price__lte=city_max)

    property_list = Property.objects.all()
    paginator = Paginator(property_list, 10)  # Show 10 properties per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if 'city' in request.GET:
        page_obj = page_obj.object_list.filter(city__icontains=request.GET['city'])
    if 'state' in request.GET:
        page_obj = page_obj.object_list.filter(state__icontains=request.GET['state'])
    # Add more filters as needed

    return render(request, 'property_list.html', {'page_obj': page_obj})



@login_required
def property_detail(request, pk):
    property = Property.objects.get(pk=pk)

    if request.method == 'POST':
        buyer = request.user
        seller_email = property.seller.email
        buyer_email = buyer.email
        send_mail(
            'Property Interest Notification',
            f'{buyer.username} is interested in your property: {property.title}.',
            'your-email@example.com',
            [seller_email],
            fail_silently=False,
        )
        send_mail(
            'Seller Contact Information',
            f'Thank you for your interest in {property.title}. Contact the seller at {seller_email}.',
            'your-email@example.com',
            [buyer_email],
            fail_silently=False,
        )

    return render(request, 'property_detail.html', {'property': property})


@login_required
def like_property(request, pk):
    property = Property.objects.get(pk=pk)
    if property.likes.filter(id=request.user.id).exists():
        property.likes.remove(request.user)
        liked = False
    else:
        property.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': property.likes.count()})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)  #compares the password and username

        if User is None:
            messages.error(request,'Invalid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/property/create/')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')