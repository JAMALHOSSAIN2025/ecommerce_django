# products/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product

# ✅ প্রোডাক্ট অ্যাড ফাংশন
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # seller হিসেবে লগইন করা ইউজার
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

# ✅ প্রোডাক্ট লিস্ট দেখানোর ফাংশন
def product_list(request):
    products = Product.objects.all().order_by('-created_at')  # নতুন প্রোডাক্ট আগে
    return render(request, 'products/product_list.html', {'products': products})

# This is a dummy comment to test Render trigger
