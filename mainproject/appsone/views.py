from multiprocessing import connection
from tempfile import template

import razorpay
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import razorpay  # Import the Razorpay Python client
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# def cart(request):
#     return render(request,"cart.html")
# def category(request):
#    return render(request,"category.html")
# def checkout(request):
#     return render(request,"checkout.html")
# def confirmation(request):
#     return render(request,"confirmation.html")
def contact(request):
    d = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=d).count()
    user = get_object_or_404(UserRegister1, id=d)


    message = Message.objects.filter(user=user)

    return render(request, "contact.html", {'cart_count': cart_count, 'user': user,'message':message})
def contact_add(request):
    d = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=d).count()
    user = get_object_or_404(UserRegister1, id=d)
    if request.method == 'POST':
        user_m = user
        subject = request.POST['subject']
        message_content = request.POST['message']
        email = request.POST['email']
        Message.objects.create(
            user=user_m,
            subject=subject,
            message=message_content,
            email=email
        )
    return render(request, "contact.html", )

def index(request):
    data = product.objects.all()
    return render(request, "index.html", {"product": data})


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user by checking the Admin model
        admin = Admin_one.objects.filter(email=email, password=password).first()
        if admin:
            request.session['admin_id'] = admin.id
            request.session['admin_name'] = admin.admin_name
            request.session['profile_pic'] = admin.profile_pic.url if admin.profile_pic else None
            request.session['email'] = admin.email
            request.session['phone_number'] = admin.phone_number
            messages.success(request, 'Admin logged in successfully.')
            return redirect('adminindex')

    return render(request, 'admin_login.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('n1', '')
        password = request.POST.get('n2', '')

        user = UserRegister1.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id  # Save user ID to session
            request.session['user_name'] = user.user_name
            request.session['profile_pic'] = user.profile_pic.url if user.profile_pic else None
            request.session['email'] = user.email
            request.session['phone_number'] = user.phone_number
            request.session['Street'] = user.Street
            request.session['House'] = user.House
            request.session['State'] = user.State
            request.session['Pin'] = user.Pin
            request.session['Country'] = user.Country

            messages.success(request, 'User logged in successfully.')
            return redirect('userindex')

        employee = ShopEmployeeRegister1.objects.filter(email=email, password=password).first()

        if employee:
            if employee.status == 'Approve':
                request.session['employee_id'] = employee.id
                request.session['employee_name'] = employee.employee_name
                request.session['profile_pic'] = employee.profile_pic.url if employee.profile_pic else None
                messages.success(request, 'Employee logged in successfully.')
                return redirect('delivery_index')
            else:
                messages.error(request, 'Your account is pending approval from the admin.')
                return redirect('login')

        messages.error(request, 'Invalid email or password.')

    return render(request, "login.html")


# def singleblog(request):
#     return render(request,"single-blog.html")
# def singleproduct(request):
#     return render(request,"single-product.html")
# def tracking(request):
#     return render(request,"tracking-oder.html")
from django.db.models import Count, Sum


def adminindex(request):
    admin_id = request.session.get('admin_id')
    admin = Admin_one.objects.get(pk=1)
    # Counting total users, employees, and products
    user_count = UserRegister1.objects.count()
    employee_count = ShopEmployeeRegister1.objects.count()
    product_count = product.objects.count()
    product_data = product.objects.all()
    messages =Message.objects.filter(status=0)
    messages_count =Message.objects.filter(status=0).count()

    # Counting the categories in user_cart
    category_counts = Paid_Product.objects.values('product_details__category').annotate(
        count=Count('product_details__category'))
    paid_products = Paid_Product.objects.all()

    # Calculate total price for all products
    total_price_all = sum(product.total_price for product in paid_products)

    print(category_counts)

    # Initializing the counts for each category
    a = b = c = 0

    # Iterating through the category counts and assigning values based on category type
    for category in category_counts:
        if category['product_details__category'] == "Headset":
            a = category['count']
        elif category['product_details__category'] == "Smart-Phone":
            b = category['count']
        else:
            c = category['count']
    print(a, b, c)

    total_quantities = Paid_Product.objects.values('product_details__id', 'product_details__p_name').annotate(
        total_quantity=Sum('quantity'))

    return render(request, "adminindex.html", {
        'user_count': user_count,
        'employee_count': employee_count,
        'product_count': product_count,
        'product_data': product_data,
        'Headset': a,
        'Smart_Phone': b,
        'Laptop': c,
        'total_price_all': total_price_all,
        "admin": admin,
        "total_quantities" : total_quantities,
        'messages':messages,
        'messages_count':messages_count
    })


def orders(request):
    admin_id = request.session.get('admin_id')
    admin = Admin_one.objects.get(pk=admin_id)
    data = Paid_Product.objects.filter(status='Paid')
    Shipped = Paid_Product.objects.filter(status='Shipped')
    Delivered = Paid_Product.objects.filter(status='Delivered')
    messages = Message.objects.filter(status=0)
    messages_count = Message.objects.filter(status=0).count()
    return render(request, "orders.html", {'cart': data, 'admin': admin, "Shipped":Shipped,"Delivered":Delivered,'messages_count':messages_count,'messages':messages})


def user_details(request):
    messages = Message.objects.filter(status=0)
    messages_count = Message.objects.filter(status=0).count()
    admin_id = request.session.get('admin_id')
    admin = Admin_one.objects.get(pk=admin_id)
    query = request.GET.get('search', '')
    if query:
        if query.isdigit():
            # If query is numeric, filter by id
            data = UserRegister1.objects.filter(id=query)
        else:
            # If query is non-numeric, filter by name (case-insensitive)
            data = UserRegister1.objects.filter(user_name=query)

    else:
        data = UserRegister1.objects.all()
    return render(request, "user_details.html", {'user': data,'admin':admin,'messages':messages,'messages_count':messages_count})


def employee_details(request):
    messages= Message.objects.filter(status=0)
    messages_count = Message.objects.filter(status=0).count
    admin_id = request.session.get('admin_id')
    admin = Admin_one.objects.get(pk=admin_id)
    query = request.GET.get('search', '')
    if query:
        if query.isdigit():
            # If query is numeric, filter by id
            data = ShopEmployeeRegister1.objects.filter(id=query)
        else:
            # If query is non-numeric, filter by name (case-insensitive)
            data = ShopEmployeeRegister1.objects.filter(employee_name__icontains=query)
    else:
        data = ShopEmployeeRegister1.objects.all()
    return render(request, "employee_details.html", {'employee': data,'admin':admin,'messages':messages,'messages_count':messages_count})


def add_category(r):
    if r.method == 'POST':
        a = r.POST['n4']
        data = add_category.objects.create(category_name=a)
        data.save()
    return render(r, "Add_product.html")


def Add_product(r):
    admin_id = r.session.get('admin_id')
    admin = Admin_one.objects.get(id=admin_id)
    messages=Message.objects.filter(status=0)
    messages_count=Message.objects.filter(status=0).count()
    if r.method == 'POST':
        a = r.POST['n1']
        b = r.POST['n2']
        c = r.POST['n3']
        d = r.POST['n4']
        e = r.FILES['n5']
        f = r.POST['n6']
        g = r.POST['n7']
        h = r.POST['n8']
        print(a, b, c, d, e, f, g, h)
        product.objects.create(p_name=a, description=b, brand=c, category=d, image=e, offer=f, price=g,
                               quantity=h).save()
        messages.success(r, 'Product added successfully!')
    return render(r, 'Add_product.html',{'messages':messages,'messages_count': messages_count,'admin':admin})


def edit_product(r, d):
    data = product.objects.get(pk=d)
    return render(r, 'update_product.html', {'product': data})


def Approve(r, d):
    print('Approve' + str(d))
    data = ShopEmployeeRegister1.objects.get(pk=d)
    data.status = 'Approve'
    data.save()

    return redirect('employee_details')


def Reject(r, d):
    data = ShopEmployeeRegister1.objects.get(pk=d)
    data.status = 'Reject'
    data.save()

    return redirect('employee_details')


def update_product(request):
    if request.method == 'POST':
        id = request.POST.get('textid')
        data = get_object_or_404(product, pk=id)
        data.p_name = request.POST.get('n1')
        data.description = request.POST.get('n2')
        data.brand = request.POST.get('n3')
        data.category = request.POST.get('n4')

        if request.FILES.get('n5'):
            data.image = request.FILES['n5']

        data.offer = request.POST.get('n6')
        data.price = request.POST.get('n7')
        data.quantity = request.POST.get('n8')

        data.save()
        messages.success(request, 'Product updated successfully')
        return redirect('Manage_Product')


def delete(r, d):
    data = product.objects.get(pk=d)
    data.delete()
    messages.success(r, 'deleted succesfully')
    return redirect('Manage_Product')


def Manage_Product(r):
    admin_id = r.session.get('admin_id')
    admin = Admin_one.objects.get(id=admin_id)
    messages=Message.objects.filter(status=0)
    messages_count=Message.objects.filter(status=0).count()
    query = r.GET.get('search', '')
    if query:
        if query.isdigit():
            # If query is numeric, filter by id
            data = product.objects.filter(id=query)
        else:
            # If query is non-numeric, filter by name (case-insensitive)
            data = product.objects.filter(
                Q(p_name__icontains=query) | Q(category__icontains=query) | Q(brand__icontains=query))

    else:
        data = product.objects.all()
    return render(r, "Manage_Product.html", {'data': data,'messages':messages,'messages_count':messages_count,'admin':admin})


def admin_profile(request):
    admin_id = request.session.get('admin_id')
    data = Admin_one.objects.get(pk=admin_id)
    return render(request, "admin_profile.html", {"admin": data})


def admin_edit(request):
    if request.method == 'POST':
        id = request.session.get('admin_id')
        data = get_object_or_404(Admin_one, pk=id)
        data.admin_name = request.POST.get('admin_name')
        data.email = request.POST.get('email')
        data.phone_number = request.POST.get('phone_number')
        data.password = request.POST.get('password')

        if request.method == 'POST':
            # Get profile_pic from request.FILES
            profile_pic = request.FILES.get('profile_pic')

            # Ensure you're handling the file upload properly in your model
            if profile_pic:
                data.profile_pic = profile_pic

            # Save admin data
            data.save()
        data.save()
        messages.success(request, 'admin updated successfully')
        return redirect('admin_profile')


def edit_admin(r):
    d = r.session.get('admin_id')
    admin = get_object_or_404(Admin_one, id=d)
    return render(r, 'admin_edit.html', {'admin': admin})


def employee_edit(request):
    if request.method == 'POST':
        id = request.session.get('employee_id')
        data = get_object_or_404(ShopEmployeeRegister1, pk=id)
        data.employee_name = request.POST.get('employee_name')
        data.email = request.POST.get('email')
        data.phone_number = request.POST.get('phone_number')
        data.password = request.POST.get('password')

        if request.method == 'POST':
            # Get profile_pic from request.FILES
            profile_pic = request.FILES.get('profile_pic')

            # Ensure you're handling the file upload properly in your model
            if profile_pic:
                data.profile_pic = profile_pic

            # Save admin data
            data.save()
        data.save()
        messages.success(request, 'admin updated successfully')
        return redirect('employee_profile')


def edit_employee(r):
    d = r.session.get('employee_id')
    employee = get_object_or_404(ShopEmployeeRegister1, id=d)
    return render(r, 'employee_edit.html', {'employee': employee})


def message(request):
    admin_id = request.session.get('admin_id')
    admin = Admin_one.objects.get(pk=admin_id)
    messages=Message.objects.filter(status=0)
    messages_count=Message.objects.filter(status=0).count()

    if request.method == 'POST':
        m_id = request.POST['id']
        reply = request.POST['reply']
        message = get_object_or_404(Message, id=m_id)
        message.reply = reply
        message.status = 1
        message.save()
    message = Message.objects.filter(status=0)

    return render(request, "messages.html",{'message':message,'messages':messages,'messages_count':messages_count,'admin':admin})


from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages


def user_reg(r):
    if r.method == "POST":
        a = r.POST['n1']  # Username
        b = r.POST['n2']  # Phone number
        c = r.POST['n3']  # Email
        d = r.POST['n4']  # Password
        e = r.POST['n5']  # Confirm Password
        f = r.POST['street']  # Street
        g = r.POST['house']  # House
        h = r.POST['state']  # State
        i = r.POST['pin']  # Pin
        j = r.POST['country']  # Country

        # Validate email format
        try:
            validate_email(c)
        except ValidationError:
            messages.error(r, 'Invalid email format')
            return render(r, "user_register.html")

        # Validate phone number length
        if len(b) != 10 or not b.isdigit():
            messages.error(r, 'Phone number must be exactly 10 digits')
            return render(r, "user_register.html")

        # Check if passwords match
        if d == e:
            # Check for unique username, email, and phone number
            if UserRegister1.objects.filter(user_name=a).exists():
                messages.error(r, 'Username already registered')
            elif UserRegister1.objects.filter(email=c).exists():
                messages.error(r, 'Email already registered')
            elif UserRegister1.objects.filter(phone_number=b).exists():
                messages.error(r, 'Phone number already registered')
            else:
                # Create and save the user if all checks pass
                data = UserRegister1.objects.create(
                    user_name=a,
                    phone_number=b,
                    email=c,
                    password=d,
                    Street=f,
                    House=g,
                    State=h,
                    Pin=i,
                    Country=j
                )
                data.save()
                messages.success(r, 'Registered successfully')
        else:
            messages.error(r, 'Password mismatch')

    return render(r, "user_register.html")


from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect, render

def employee_register(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirmPassword', '').strip()

        # Name validation: Check if name is not empty
        if not name:
            messages.error(request, 'Name is required.')
            return render(request, 'employee_register.html')

        # Phone number validation: Check if it's exactly 10 digits and only numbers
        if len(phone_number) != 10 or not phone_number.isdigit():
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'employee_register.html')

        # Email validation: Check if email format is valid
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return render(request, 'employee_register.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'employee_register.html')

        # Check uniqueness of name, email, and phone number
        if ShopEmployeeRegister1.objects.filter(name=name).exists():
            messages.error(request, 'Name already registered.')
            return render(request, 'employee_register.html')
        elif ShopEmployeeRegister1.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'employee_register.html')
        elif ShopEmployeeRegister1.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number already registered.')
            return render(request, 'employee_register.html')

        # Store data in session for later use if all validations pass
        request.session['registration_data'] = {
            'name': name,
            'phone_number': phone_number,
            'email': email,
            'password': password
        }

        return redirect('employee_register_2')

    return render(request, "employee_register.html")


def employee_register_2(request):
    if request.method == "POST":
        registration_data = request.session.get('registration_data', {})
        print(registration_data)
        if not registration_data:
            messages.error(request, 'No registration data found.')
            return redirect('employee_register')

        licence = request.FILES.get('license')
        psp = request.FILES.get('passport_photo')

        ShopEmployeeRegister1.objects.create(
            user_type='employee',
            employee_name=registration_data.get('name'),
            phone_number=registration_data.get('phone_number'),
            email=registration_data.get('email'),
            password=registration_data.get('password'),
            licence=licence,
            psp=psp,
            status='Pending',
            profile_pic=''

        )

        del request.session['registration_data']

        messages.success(request, 'Registration successful. Awaiting admin approval.')
        return redirect('login')
    return render(request, "employee_register_2.html")


def userindex(request):
    d = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=d).count()
    user = get_object_or_404(UserRegister1, id=d)
    data = product.objects.all()
    ads = Advertisements.objects.all()

    return render(request, "userindex.html", {'user': user, 'product': data, 'cart_count': cart_count,'ads':ads })


def delivery_index(request):
    employee_id = request.session.get('employee_id')
    employee = get_object_or_404(ShopEmployeeRegister1, id=employee_id)
    product_shipped = Paid_Product.objects.filter(status='Shipped').count()
    product_delivered = Paid_Product.objects.filter(status='Delivered').count()
    product_delivered_data = Paid_Product.objects.filter(status='Delivered')

    # Prepare context dictionary with the employee data
    context = {
        'employee': employee,
        'product_shipped':product_shipped,
        'product_delivered':product_delivered,
        'product_delivered_data':product_delivered_data

    }

    return render(request, "delivery_index.html", context)


def user_profile(request):
    d = request.session.get('user_id')
    print(d)
    user = get_object_or_404(UserRegister1, id=d)

    return render(request, "user_profile.html", {'user': user})


def delivery_boy_profile(request):
    return render(request, "delivery_boy_profile.html")


def delivery_orders(request):
    employee_id = request.session.get('employee_id')
    employee = get_object_or_404(ShopEmployeeRegister1, id=employee_id)

    Shipped = Paid_Product.objects.filter(status='Shipped')
    Delivered = Paid_Product.objects.filter(status='Delivered')


    # Prepare context dictionary with the employee data
    context = {
        'employee': employee,
        'Shipped' : Shipped,
        'Delivered':Delivered

    }
    return render(request, "delivery_orders.html", context)


def employee_profile(request):
    employee_id = request.session.get('employee_id')
    employee = get_object_or_404(ShopEmployeeRegister1, id=employee_id)

    context = {
        'employee': employee,
    }
    return render(request, "employee_profile.html", context)


def category(request):
    return render(request, "category.html")


def user_category(request):
    d = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=d).count()
    print(d)
    user = get_object_or_404(UserRegister1, id=d)
    data = product.objects.all()

    return render(request, "user_category.html", {'user': user, 'cart_count': cart_count,'products':data})


def add_cart(r, d):
    a = r.session.get('user_id')
    print("-" + str(d))
    data = product.objects.get(pk=d)
    user = get_object_or_404(UserRegister1, id=a)
    if user_cart.objects.filter(product_details=d, user_details=user).exists():
        d1 = user_cart.objects.get(product_details=d, user_details=user)
        print(d1)
        d1.quantity += 1
        print(d1)
        d1.save()
        return redirect('cart')
    else:
        user_cart.objects.create(product_details=data, user_details=user).save()
        messages.success(r, 'added to cart')
        return redirect('cart')


def cart(request):
    a = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=a).count()

    user = get_object_or_404(UserRegister1, id=a)
    data = user_cart.objects.filter(user_details=user)
    for item in user_cart.objects.all():
        item.total_price = item.product_details.price * item.quantity
        item.save()

    # Initialize subtotal
    subtotal = 0
    # Calculate total for each item and the subtotal
    for item in data:
        item_total = item.product_details.price * item.quantity
        subtotal += item_total

        item.save()

    context = {
        'data': data,
        'user': user,
        'subtotal': subtotal,
        'cart_count': cart_count
    }

    return render(request, "cart.html", context)


def remove_cart(r, d):
    data = user_cart.objects.get(pk=d)
    data.delete()
    messages.success(r, 'Removed wishlist')
    return redirect('cart')


def multiply(value, arg):
    return value * arg


def increment(r, d):
    item = get_object_or_404(user_cart, id=d)
    item.quantity += 1
    item.save()
    return redirect('cart')  # Replace 'cart' with your cart page URL name


def decrement(r, d):
    item = get_object_or_404(user_cart, id=d)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart')


def add_wishlist(r, d):
    a = r.session.get('user_id')
    data = product.objects.get(pk=d)
    user = get_object_or_404(UserRegister1, id=a)
    if wishlist.objects.filter(product_details_id=d, user_details=user).exists():
        return redirect('user_wish')
    else:
        wishlist.objects.create(product_details=data, user_details=user).save()
        messages.success(r, 'added to wishlist')
        return redirect('user_wish')


def user_wish(request):
    a = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=a).count()
    user = get_object_or_404(UserRegister1, id=a)
    data = wishlist.objects.filter(user_details=user)
    return render(request, 'user_wish.html', {'data': data, 'user': user, 'cart_count': cart_count})


def remove_wishlist(r, d):
    data = wishlist.objects.get(pk=d)
    data.delete()
    messages.success(r, 'Removed wishlist')
    return redirect('user_wish')


def payment(request, data1):
    amount = data1
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    cursor = connection.cursor()
    a = request.session.get('user_id')
    user = get_object_or_404(UserRegister1, id=a)
    data = user_cart.objects.filter(user_details=user)

    data.update(status='paid')
    id = request.session.get("user_id")
    user = UserRegister1.objects.filter(id=id)
    cart = user_cart.objects.filter(user_details=a)

    # cursor.execute("update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(id) + "' ")

    payment_order = client.order.create({
        'amount': amount,
        'currency': order_currency,
        'payment_capture': '1'
    })

    # Pass order details to the template
    context = {
        'payment': payment_order,
        'amount': amount,
        'cart': cart
    }
    return render(request, "payment.html", context)


def payment2(request, data1):
    amount = data1
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    cursor = connection.cursor()
    a = request.session.get('user_id')
    user = get_object_or_404(UserRegister1, id=a)
    data = user_cart.objects.filter(user_details=a)

    data.update(status='paid')
    id = request.session.get("user_id")
    user = UserRegister1.objects.filter(id=id)
    cart = user_cart.objects.filter(user_details=user)

    # cursor.execute("update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(id) + "' ")

    payment_order = client.order.create({
        'amount': amount,
        'currency': order_currency,
        'payment_capture': '1'
    })

    # Pass order details to the template
    context = {
        'payment': payment_order,
        'amount': amount,
        'cart': cart
    }
    return render(request, "payment2.html", context)


def single_product(request, d):
    data2 = product.objects.all()
    a = request.session.get('user_id')
    user = get_object_or_404(UserRegister1, id=a)
    data = product.objects.get(pk=d)
    data1 = data.quantity
    data3 = data.quantity
    if data1 == 0:
        Stock = "Out Of Stock"
    else:
        Stock = "In Stock"
    return render(request, "single_product.html",
                  {'data': data, 'user': user, 'Stock': Stock, "product": data2, "availibility": data3})


def confirmation(request, d):
    a = request.session.get('user_id')
    user = get_object_or_404(UserRegister1, id=a)
    data = product.objects.get(pk=d)
    if data:
        request.session['single_product_id'] = data.id
    data1 = data.price + 50
    return render(request, "confirmation.html", {'user': user, 'data': data, 'data1': data1})


def confirmation_cart(request):
    a = request.session.get('user_id')
    user = get_object_or_404(UserRegister1, id=a)
    data = user_cart.objects.filter(user_details=user)
    subtotal = 0
    # Calculate total for each item and the subtotal
    for item in data:
        item_total = item.product_details.price * item.quantity
        subtotal += item_total
        data1 = subtotal + 50

    context = {
        'data': data,
        'user': user,
        'subtotal': subtotal,
        'data1': data1,

    }
    print(context)

    return render(request, "confirmation_cart.html", context)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def user_edit(request):
    if request.method == 'POST':
        id = request.session.get('user_id')
        data = get_object_or_404(UserRegister1, pk=id)

        # Update text fields
        data.user_name = request.POST.get('user_name')
        data.email = request.POST.get('email')
        data.phone_number = request.POST.get('phone_number')
        data.Street = request.POST.get('Street')
        data.House = request.POST.get('House')
        data.State = request.POST.get('State')
        data.Pin = request.POST.get('Pin')
        data.Country = request.POST.get('Country')
        data.password = request.POST.get('password')

        # Update profile picture if a new one is uploaded
        if request.FILES.get('profile_pic'):
            data.profile_pic = request.FILES['profile_pic']

        data.save()
        messages.success(request, 'User updated successfully')
        return redirect('user_profile')

    return render(request, 'user_edit.html')


def edit_user(r):
    d = r.session.get('user_id')
    print(d)
    user = get_object_or_404(UserRegister1, id=d)
    return render(r, 'user_edit.html', {'user': user})


def search_page(request):
    query = request.GET.get('searchQueryInput')  # Get the search query from the form input
    p_data = product.objects.all()  # Get all products for category display
    d = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=d).count()
    print(d)
    user = get_object_or_404(UserRegister1, id=d)

    if query:
        # Filter products based on product name, category, or brand containing the search term
        data = product.objects.filter(
            Q(p_name__icontains=query) | Q(category__icontains=query) | Q(brand__icontains=query)
        )
    else:
        # If no query, return all products
        data = product.objects.all()

    # Get unique categories to display on the page
    categories = product.objects.values_list('category', flat=True).distinct()

    return render(request, "search_page.html", {
        'data': data,
        'p_data': p_data,
        'categories': categories , # Pass categories to the template
        'cart_count' : cart_count,
        'user':user
    })


def product_list_view(request):
    d = request.session.get('user_id')
    cart_count = user_cart.objects.filter(user_details=d).count()
    print(d)
    user = get_object_or_404(UserRegister1, id=d)
    # Get query parameters for filtering and sorting
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')
    sort_order = request.GET.get('sort', 'asc')  # Default to ascending order

    # Get price range filter
    lower_price = request.GET.get('lower_price')
    upper_price = request.GET.get('upper_price')

    # Filter products based on the selected brand and category
    products = product.objects.all()

    if brand_filter:
        products = products.filter(brand=brand_filter)
    if category_filter:
        products = products.filter(category=category_filter)

    # Filter by price range if provided
    if lower_price and upper_price:
        products = products.filter(price__gte=lower_price, price__lte=upper_price)

    # Make sure the queryset is distinct (no duplicates)
    products = products.distinct()

    # Sorting products
    if sort_order == 'asc':
        products = products.order_by('price')
    else:
        products = products.order_by('-price')

    # Retrieve distinct categories and brands to avoid repetition in the template
    distinct_brands = products.values_list('brand', flat=True).distinct()
    distinct_categories = products.values_list('category', flat=True).distinct()

    # Context to be passed to template
    context = {
        'products': products,
        'brands': distinct_brands,
        'categories': distinct_categories,
        'user': user,
        'cart_count': cart_count
    }
    return render(request, 'user_category.html', context)


def user_order(request):
    user_id = request.session.get("user_id")
    cart_count = user_cart.objects.filter(user_details=user_id).count()

    try:
        user = UserRegister1.objects.get(id=user_id)  # Get user object
        orders = Paid_Product.objects.filter(user_details=user).order_by('-id')    # Get all paid products for the user

        context = {
            'user': user,
            'orders': orders,
            'cart_count':cart_count# Pass orders to the template
        }
        return render(request, 'user_order.html', context)

    except UserRegister1.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')


def paid_cart(request):
    # Retrieve the user ID from the session
    user_id = request.session.get("user_id")

    try:
        # Get the user object
        user = UserRegister1.objects.get(id=user_id)

        # Get all items from the user's cart
        cart_items = user_cart.objects.filter(user_details=user_id)

        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart_view')

        # Loop through each cart item to create Paid_Product entries
        for cart_item in cart_items:
            paid_product = Paid_Product(
                product_details=cart_item.product_details,
                user_details=user,
                status='Paid',
                quantity=cart_item.quantity

            )
            cart_product_id = cart_item.product_details.id
            product_items = product.objects.get(id=cart_product_id)
            main_product_quantity = product_items.quantity
            update_quantity = main_product_quantity - cart_item.quantity
            product_items.quantity = update_quantity
            product_items.save()

            paid_product.save()

        # Clear the cart after saving
        cart_items.delete()
        orders = Paid_Product.objects.filter(user_details=user)
        cart_count = user_cart.objects.filter(user_details=user_id).count()

        return render(request, 'user_order.html', {'message': 'Order placed successfully!','orders':orders,'cart_count':cart_count,'user':user})

    except UserRegister1.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('cart')


def paid_single_product(request):
    user_id = request.session.get("user_id")
    product_id = request.session.get("single_product_id")
    u = UserRegister1.objects.get(id=user_id)
    p = product.objects.get(id=product_id)
    paid_product = Paid_Product(
        product_details=p,
        user_details=u,
        status='Paid',
        quantity = 1
    )
    p.quantity -=1
    p.save()
    paid_product.save()
    orders = Paid_Product.objects.filter(user_details=u)
    cart_count = user_cart.objects.filter(user_details=user_id).count()

    return render(request, 'user_order.html', {'message': 'Order placed successfully!','orders':orders,'cart_count':cart_count,'user':u})


def dispatch_order(request, id):
    # Get the Paid_Product instance or return a 404 if it doesn't exist
    paid_product = get_object_or_404(Paid_Product, id=id)

    # Update the status
    paid_product.status = "Shipped"
    paid_product.save()

    # Optionally, you can add a success message here or redirect to another page
    return redirect('orders')

def dispatch_order_delivered(request,id):
    paid_product = get_object_or_404(Paid_Product, id=id)

    # Update the status
    paid_product.status = "Delivered"
    paid_product.save()
    return redirect('delivery_orders')



def Ads(r):
    admin_id = r.session.get('admin_id')
    admin = Admin_one.objects.get(id=admin_id)
    messages=Message.objects.filter(status=0)
    messages_count=Message.objects.filter(status=0).count()
    if r.method == 'POST':
        a = r.POST['n1']
        b = r.POST['n2']
        c = r.POST['n3']
        d = r.FILES['n5']

        print(a, b, c, d,)
        Advertisements.objects.create(p_name=a, heading=b, subheading=c, image=d).save()

    return render(r, 'Ads.html',{'messages':messages,'messages_count': messages_count,'admin':admin})



def Manage_Ads(r):
    admin_id = r.session.get('admin_id')
    admin = Admin_one.objects.get(id=admin_id)
    messages=Message.objects.filter(status=0)
    messages_count=Message.objects.filter(status=0).count()
    query = r.GET.get('search', '')
    if query:
        if query.isdigit():
            # If query is numeric, filter by id
            data = Advertisements.objects.filter(id=query)
        else:
            # If query is non-numeric, filter by name (case-insensitive)
            data = Advertisements.objects.filter(
                Q(p_name__icontains=query) | Q(category__icontains=query) | Q(brand__icontains=query))

    else:
        data = Advertisements.objects.all()
    return render(r, "Manage_Ads.html", {'data': data,'messages':messages,'messages_count':messages_count,'admin':admin})


def delete_ads(r, d):
    data = Advertisements.objects.get(pk=d)
    data.delete()
    messages.success(r, 'deleted succesfully')
    return redirect('Manage_Ads')


from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from .models import UserRegister1, ShopEmployeeRegister1, PasswordResetToken


def request_password_reset(request):
    sent = False
    error = None
    if request.method == 'POST':
        email = request.POST['email']
        user = UserRegister1.objects.filter(email=email).first() or ShopEmployeeRegister1.objects.filter(
            email=email).first()

        if user:
            token = PasswordResetToken.objects.create(user_email=email)
            reset_link = request.build_absolute_uri(reverse('password_reset_form', args=[str(token.token)]))


            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_link}',
                'vivekrajve@gmail.com',  # Replace with your email
                [email],
            )
            sent = True
        else:
            error = 'Email not found.'

    return render(request, 'forgot_password.html', {'sent': sent, 'error': error})


def password_reset_form(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token, is_active=True)
    reset_success = False

    if request.method == 'POST':
        new_password = request.POST['password']
        user = UserRegister1.objects.filter(email=token_obj.user_email).first() or ShopEmployeeRegister1.objects.filter(
            email=token_obj.user_email).first()

        if user:
            user.password = new_password
            user.save()
            token_obj.is_active = False
            token_obj.save()
            reset_success = True

            # Add success message
            messages.success(request, 'Your password has been reset successfully! You can now log in with your new password.')
        else:
            # Add error message if user is not found
            messages.error(request, 'We could not find a user associated with this token. Please try again.')

    # Render the password reset form template with the success flag
    return render(request, 'password_reset_form.html', {'reset_success': reset_success})


