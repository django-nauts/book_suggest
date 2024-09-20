from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken


class SuperUserLoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return JsonResponse({'error': 'Invalid credentials or not a superuser'}, status=403)
