from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>স্বাগতম আমার Django প্রোজেক্টে!</h1><p>এটা হোম পেজ।</p>")
