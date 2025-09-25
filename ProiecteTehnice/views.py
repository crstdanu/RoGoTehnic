from django.shortcuts import render

# Create your views here.


def index_PTH(request):
    return render(request, 'ProiecteTehnice/index.html')
