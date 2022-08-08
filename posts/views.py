from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, template_name='posts/home.html', context=context)
