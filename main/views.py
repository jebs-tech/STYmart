import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

from main.models import Product
from main.forms import ProductForm

# ----------------- MAIN -----------------
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "my":
        product_list = Product.objects.filter(user=request.user)
    else:
        product_list = Product.objects.all()

    context = {
        "app_name": "STYMart",
        "npm": "2406431334",
        "name": request.user.username,
        "class": "PBP F",
        "product_list": product_list,
        "last_login": request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

# ----------------- AUTH -----------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {"form": form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect('/main/')
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('last_login')
    return response


# ----------------- AJAX CRUD -----------------
@csrf_exempt
@require_POST
@login_required(login_url='/login')
def create_product_ajax(request):
    """Create new product via AJAX"""
    name = request.POST.get('name')
    price = request.POST.get('price', 0)
    description = request.POST.get('description', '')
    stock = request.POST.get('stock', 0)
    category = request.POST.get('category', '')
    thumbnail = request.POST.get('thumbnail', '')
    color = request.POST.get('color', '')
    size = request.POST.get('size', '')
    is_featured = request.POST.get('is_featured') == 'on'

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        return JsonResponse({'error': 'Invalid numeric input'}, status=400)

    product = Product.objects.create(
        name=name,
        price=price,
        description=description,
        stock=stock,
        category=category,
        thumbnail=thumbnail,
        color=color,
        size=size,
        is_featured=is_featured,
        user=request.user
    )

    return JsonResponse({'status': 'created', 'product_id': product.id}, status=201)


@csrf_exempt
@require_POST
@login_required(login_url='/login')
def edit_product_ajax(request, product_id):
    """Edit product via AJAX"""
    product = get_object_or_404(Product, pk=product_id)

    if product.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    name = request.POST.get('name', product.name)
    price = request.POST.get('price', product.price)
    description = request.POST.get('description', product.description)
    stock = request.POST.get('stock', product.stock)
    category = request.POST.get('category', product.category)
    thumbnail = request.POST.get('thumbnail', product.thumbnail)
    color = request.POST.get('color', product.color)
    size = request.POST.get('size', product.size)
    is_featured = request.POST.get('is_featured') == 'on'

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        return JsonResponse({'error': 'Invalid numeric input'}, status=400)

    product.name = name
    product.price = price
    product.description = description
    product.stock = stock
    product.category = category
    product.thumbnail = thumbnail
    product.color = color
    product.size = size
    product.is_featured = is_featured
    product.save()

    return JsonResponse({'status': 'updated', 'product_id': product.id}, status=200)


@csrf_exempt
@require_POST
@login_required(login_url='/login')
def delete_product_ajax(request, product_id):
    """Delete product via AJAX"""
    product = get_object_or_404(Product, pk=product_id)

    if product.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    product.delete()
    return JsonResponse({'status': 'deleted', 'product_id': product_id}, status=200)


# ----------------- JSON Endpoint -----------------
@login_required(login_url='/login')
def show_json_by_id(request):
    """List all products as JSON (with optional filter=my)"""
    filter_type = request.GET.get("filter", "all")
    if filter_type == "my":
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()

    data = [
        {
            'id': p.id,
            'name': p.name,
            'price': float(p.price) if p.price else 0,
            'description': p.description,
            'stock': p.stock,
            'category': p.category,
            'thumbnail': p.thumbnail,
            'color': p.color,
            'size': p.size,
            'is_featured': p.is_featured,
            'user_id': p.user.id if p.user else None,
            'user_username': p.user.username if p.user else None,
        }
        for p in products
    ]

    return JsonResponse(data, safe=False)

def show_xml(request):
     product_list = Product.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
   try:
       product_item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)