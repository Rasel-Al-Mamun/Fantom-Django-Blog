from django.shortcuts import render


def homeView(request):
    home = "home"
    context = {
        'home': home,
    }
    return render(request, 'home/index.html', context)
