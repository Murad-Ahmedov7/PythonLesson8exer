from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello Django!")


# def home(request):
#     context = {"name": "Elvin", "course": "Python Web"}
#     return render(request, "home.html", context)

def home(request,username="User"):
    context = {"name": username, "course": "Python Web"}
    return render(request, "home.html", context)

def students(request):
    context={
        "students":['Elvin','Aysel','John'],
        "show":True
    }

    return render(request,"students.html",context)