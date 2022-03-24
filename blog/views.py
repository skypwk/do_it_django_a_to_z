from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin



class PostList(ListView):
    model = Post
    # template_name = 'blog/index.html'
    ordering = '-pk'


    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        print("skypwk form_valid")
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            print(form.instance.title)
            return super(PostCreate, self).form_valid(form)
        return redirect('/blog/')


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context





def category_page(request, slug):

    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)




    return render(
            request,
            'blog/post_list.html',
            {
                'post_list': post_list,
                'categories': Category.objects.all(),
                'no_category_post_count': Post.objects.filter(category=None).count(),
                'category': category,

            }
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )



# def index(request):
#
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(request,
#                   'blog/index.html',
#                   {'posts': posts},
#                   )




# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request, 'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )

# Create your views here.
