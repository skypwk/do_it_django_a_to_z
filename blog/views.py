from django.shortcuts import render

# from django.http import HttpResponse

from .models import Post


def index(request):
    # return HttpResponse("안녕하세요 blog에 오신걸 환영합니다.")\
    # return render(request, 'blog/index.html',)

    posts = Post.objects.all().order_by('-pk')

    return render(request,
                  'blog/index.html',
                  {'posts': posts},
                  )


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request, 'blog/single_post_page.html',
        {
            'post': post,
        }
    )

# Create your views here.
