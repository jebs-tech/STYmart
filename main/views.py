from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .forms import ProductForm
from .models import Product
from decimal import Decimal



# ---------- Normal Page Views ---------- #

@login_required(login_url='/login/')
def show_main(request):
    filter_by = request.GET.get('filter', 'my') 
    if filter_by == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)
    context = {
        'products': products,
    }
    context.update(get_product_choices())
    return render(request, 'main.html', context)


@login_required(login_url='/login/')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'product_detail.html', {'product': product})

@login_required(login_url='/login/')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            
            product.save()
            
            return redirect('main:show_main')
        else:
            return render(request, 'create_product.html')

    context = get_product_choices()
    return render(request, 'create_product.html')


@login_required(login_url='/login/')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():
            form.save() 
            return redirect('main:show_main')
        else:
            return render(request, 'edit_product.html', {'product': product, 'form': form})
            
    form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'product': product, 'form': form})


@login_required(login_url='/login/')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product.delete()
    return redirect('main:show_main')


# ---------- Data Views (JSON/XML) ---------- #

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, product_id):
    data = Product.objects.filter(pk=product_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_by_id(request, product_id):
    data = Product.objects.filter(pk=product_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


# ---------- Auth Views (Normal) ---------- #

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:login_user")
    return render(request, "register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main:show_main")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("main:login_user")

@login_required(login_url='/login/')
def add_products_entry_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "error", 
            "message": "User not authenticated."
        }, status=401)

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({
                "status": "success",
                "message": f"Product '{product.name}' created successfully!",
                "id": product.id
            })
        else:
            return JsonResponse({
                "status": "error",
                "message": "Form data is invalid.",
                "errors": form.errors
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=400)


@csrf_exempt
@login_required(login_url='/login/')
def update_product_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "User not authenticated."}, status=401)
    try:
        product = Product.objects.get(pk=id, user=request.user)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Not found."}, status=404)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    "status": "success",
                    "message": f"Product '{product.name}' updated successfully!"
                })
            else:
                return redirect('main:show_main')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    "status": "error",
                    "message": "Form data is invalid.",
                    "errors": form.errors
                }, status=400)
            else:
                return render(request, 'edit_product.html', {'product': product, 'form': form})

    # Jika bukan POST
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=400)


@csrf_exempt
def delete_product_ajax(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return JsonResponse({"status": "deleted"})
    return HttpResponseNotAllowed(['POST'])


# ---------- AJAX Auth Views ---------- #

@csrf_exempt
def login_ajax(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "failed"})
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def register_ajax(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            return JsonResponse({"status": "error", "message": "Invalid input"})
        user = UserCreationForm({'username': username, 'password1': password, 'password2': password})
        if user.is_valid():
            user.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "failed", "errors": user.errors})
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def logout_ajax(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"status": "logged_out"})
    return HttpResponseNotAllowed(['POST'])

# ---------- Helper Cart View ---------- #
@login_required(login_url='/login/')
def add_to_cart(request, id):
    return redirect('main:show_product', id=id)

def get_product_choices():
    return {
        'all_categories': list(Product.objects.values_list('category', flat=True).distinct().order_by('category')),
        'all_colors': list(Product.objects.values_list('color', flat=True).distinct().order_by('color')),
        'all_sizes': list(Product.objects.values_list('size', flat=True).distinct().order_by('size')),
    }