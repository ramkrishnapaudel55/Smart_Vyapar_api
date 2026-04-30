from django.shortcuts import render

def server_status(request):
    return render(request, "status/server_status.html")
