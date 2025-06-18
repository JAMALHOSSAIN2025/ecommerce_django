from django.http import JsonResponse

def order_list(request):
    return JsonResponse({'message': 'Order list API works!'})
