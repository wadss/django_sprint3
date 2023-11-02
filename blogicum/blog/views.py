from django.shortcuts import get_object_or_404, render

from datetime import datetime

from blog.models import Post, Category

QNTT_POSTS = 5


def query_set():
    query = Post.objects.select_related(
        'category', 'author', 'location').filter(
            pub_date__lte=datetime.now(),
            category__is_published=True,
            is_published=True,
        )
    return query


def index(request):
    template = 'blog/index.html'
    posts_list = query_set()[:QNTT_POSTS]
    context = {'post_list': posts_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    posts_list = get_object_or_404(
        query_set(), pk=post_id)
    context = {'post': posts_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects,
        is_published=True,
        slug=category_slug
        )
    posts = query_set().filter(
        category=category)
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)
