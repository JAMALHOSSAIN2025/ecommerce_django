# 📁 products/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Product
from .forms import ProductForm
from .serializers import ProductSerializer

# ---------- UI Views ----------

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.user = request.user  # optional if needed
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})


# ---------- API Views ----------

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list_api(request):
    products = Product.objects.all().order_by('-created_at')
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)
