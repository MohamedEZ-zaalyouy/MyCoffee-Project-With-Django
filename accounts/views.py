from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .models import UserProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from products.models import Product
# Create your views here.

##########################################
# Start Sign Up Views
##########################################
def signup(request):
    if request.POST and 'btnsignup' in request.POST:

        terms = None
        is_added = None
        #Get Values from the Form
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in First Name')

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in Last Name')
        
        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request, 'Error in Address')
        
        if 'address2' in request.POST: address2 = request.POST['address2']
        else: messages.error(request, 'Error in Address2')
        
        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request, 'Error in City')
        
        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request, 'Error in State')
        
        if 'zip' in request.POST: zip = request.POST['zip']
        else: messages.error(request, 'Error in zip number')
        
        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in Email')
        
        if 'username' in request.POST: username = request.POST['username']
        else: messages.error(request, 'Error in username')
        
        if 'password' in request.POST: password = request.POST['password']
        else: messages.error(request, 'Error in Password')
        
        if 'terms' in request.POST: terms = request.POST['terms']


        # check the values:
        if fname and lname and address and address2 and city and state and zip and email and username and password:
            if terms =='on':
                # Check if Username exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This username is Taken')
                else:
                    # Check if Email exists
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is Taken')
                    else:
                        # Check if Email est valid
                        try:
                            validate_email(email)
                        except ValidationError:
                            messages.error(request, 'Invalid Email')
                            return redirect('signup')
                          
                        # Add user
                        user = User.objects.create_user(first_name = fname, last_name = lname, email=email,username=username, password=password)
                        user.save()
                        # add User Profile
                        userprofile = UserProfile(user = user, address=address, address2=address2, city=city, state=state, zip_number = zip )
                        userprofile.save()
                        #clear fields
                        fname = ''
                        lname = ''
                        address = ''
                        address2 = ''
                        city = ''
                        state = ''
                        zip = ''
                        email = ''
                        username = ''
                        password = ''
                        #Success Message
                        messages.success(request, 'Your account is created -- Tank You-- ')

                        # user is add successfully
                        is_added = True
                        
            else:
                messages.error(request, 'You must agree to the terms')
        else:
            messages.error(request, 'Check empty fields')

        context ={
              'fname': fname,
              'lname': lname,
              'address': address,
              'address2': address2,
              'city': city,
              'state': state,
              'zip': zip,
              'email': email,
              'username': username,
              'password': password,
              'is_added' :is_added,
        }
        return render(request,'accounts/signup.html',context)
    else:
        return render(request,'accounts/signup.html')
    
##########################################
# Start Sign In Views
##########################################

def signin(request):
    if request.method == 'POST' and 'btnlogin' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        

        user = authenticate(username = username , password = password)
        if user is not None:
            # Remember me
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)

            login(request, user)
            messages.success(request,'You are now logged in')
            #return redirect('/')
        else:
            messages.error(request,'Username Or Password Invalid')

        return redirect('signin')
    else:
        return render(request,'accounts/signin.html')
    

##########################################
# Start Log Out  Views
##########################################
@login_required(login_url='signin')
def LogOut(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')

##########################################
# Start Profile  Views
##########################################
@login_required(login_url='signin')
def profile(request):

    if request.POST  and 'btnSave' in request.POST:
        #Get Values from the Form
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in First Name')

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in Last Name')
        
        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request, 'Error in Address')
        
        if 'address2' in request.POST: address2 = request.POST['address2']
        else: messages.error(request, 'Error in Address2')
        
        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request, 'Error in City')
        
        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request, 'Error in State')
        
        if 'zip' in request.POST: zip = request.POST['zip']
        else: messages.error(request, 'Error in zip number')
        
        if 'password' in request.POST: password = request.POST['password']
        else: messages.error(request, 'Error in Password')

        # check the values:
        if fname and lname and address and address2 and city and state and zip and password:
            userprofile = UserProfile.objects.get(user = request.user)
            request.user.first_name = fname
            request.user.last_name = lname
            userprofile.address = address
            userprofile.address2 = address2
            userprofile.state = state
            userprofile.city = city
            userprofile.zip_number = zip
            request.user.set_password(password)

            request.user.save()
            userprofile.save()

            # login
            login(request, request.user)

            messages.success(request, 'Your data has been saved')

        else:
            messages.error(request, 'Check empty fields')

        return redirect('profile')
    else:
        # send information
        if request.user is not None:
            userprofile = UserProfile.objects.get(user = request.user)
            context = {
                'fname': request.user.first_name,
                'lname': request.user.last_name,
                'address': userprofile.address,
                'address2': userprofile.address2,
                'state': userprofile.state,
                'city': userprofile.city,
                'zip': userprofile.zip_number,
                'username': request.user.username,
                'email': request.user.email,
            }
        else:
            return redirect('/')
        return render(request,'accounts/profile.html',context)
    

##########################################
# Start add_product_favorites  Views
##########################################
@login_required(login_url='signin')
def add_product_favorites(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        #Product favorites
        pro_fav = Product.objects.get(id = pro_id)

        if UserProfile.objects.filter(user = request.user, product_favorites = pro_fav):
            userprofile = UserProfile.objects.get(user = request.user, product_favorites = pro_fav)
            userprofile.product_favorites.remove(pro_fav)
            userprofile.save() 
            messages.success(request, 'Product has been delete')
        else:
            userprofile = UserProfile.objects.get(user = request.user)
            userprofile.product_favorites.add(pro_fav)
            userprofile.save() 
            messages.success(request, 'Product has been favorite ')
        
    else:
        messages.error(request, 'You must be logged in')

    return redirect('/product/'+str(pro_id))


##########################################
# Start product favorites  Views
##########################################
@login_required(login_url='signin')
def product_favorites(request):

    userprofile = UserProfile.objects.get(user = request.user)
    pro_fav = userprofile.product_favorites.all()
    context = {
        'pro_fav':pro_fav
    }
    return render(request, 'accounts/product_favorites.html', context)