from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from datetime import datetime


def index(request):
    template = 'blog/index.html'
    posts_list = Post.objects.select_related(
        'category'
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {'post_list': posts_list}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    posts_list = get_object_or_404(
        Post.objects.select_related(
            'category'
        ).filter(
            pub_date__lt=datetime.now(),
            category__is_published=True
        ).exclude(
            is_published=False
        ), pk=pk)
    context = {'post': posts_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.filter(
        is_published=True), slug=category_slug)
    posts = Post.objects.filter(
        category=category,
        pub_date__lte=datetime.now(),
        is_published=True)
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)
