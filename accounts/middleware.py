# accounts/middleware.py

from django.shortcuts import redirect

class GoogleLoginRedirectMiddleware:
    """
    যদি ইউজার authenticated হয় এবং তার ফোন নম্বর না থাকে,
    তাহলে তাকে 'complete-profile' রিডাইরেক্ট করবে (সাধারণত Google login করা ইউজারদের জন্য)।
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # সুপারইউজার বা অ্যাডমিন প্যানেলের জন্য রিডাইরেক্ট প্রযোজ্য নয়
        if request.user.is_authenticated and not request.user.is_superuser:
            # অ্যাডমিন প্যানেল access দিলে কোনো রিডাইরেক্ট করবে না
            if request.path.startswith('/admin/'):
                return self.get_response(request)

            # যদি ফোন নম্বর না থাকে এবং প্রোফাইল রিডাইরেক্ট রুটে না থাকে
            try:
                if not request.user.phone_number:
                    if not request.path.startswith('/api/accounts/complete-profile/'):
                        return redirect('/api/accounts/complete-profile/')
            except AttributeError:
                # যদি user.phone_number না পাওয়া যায়
                pass

        return self.get_response(request)
