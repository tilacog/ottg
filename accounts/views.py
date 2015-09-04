from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def persona_login(request):
    # This is an Ajax view, so it does't need to return HTMK, just an 'OK'
    # string will do.
    user = authenticate(assertion=request.POST['assertion'])
    if user:
        login(request, user)
    return HttpResponse('OK')
