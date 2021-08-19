from django.shortcuts import render
from blog.models import Post

def homeView(request):
    home = "home"
    posts = Post.postobjects.all()
    sliders = Post.postobjects.all().order_by('-id')[:5]
    context = {
        'home': home,
        'posts': posts,
        'sliders': sliders,
    }
    return render(request, 'home/index.html', context)
