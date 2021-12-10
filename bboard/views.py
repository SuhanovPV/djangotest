from django.http import HttpResponse


def index(request):
    print("="*30)
    print(request)
    print("="*30)
    return HttpResponse("<h1>🦄</h1><p>Here will be BBOARD soon!<p><h2>🐉</h2>")
