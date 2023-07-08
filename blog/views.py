import folium

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from blog.models import Comment
from blog.models import Post
from sensive_blog.settings import COMPANY_COORDINATES


def serialize_post(post):
    """Post data serializer"""
    return {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments_amount": Comment.objects.filter(post=post).count(),
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
    }


def index(request):
    """Main page representation view"""
    all_posts = Post.objects.prefetch_related('author')
    popular_posts = all_posts.annotate(likes_count=Count('likes')).order_by('-likes_count')[:3]
    fresh_posts = all_posts.order_by('-published_at')[:5]

    context = {
        "page_title": "Main page",
        "most_popular_posts": [serialize_post(post) for post in popular_posts],
        "fresh_posts": [serialize_post(post) for post in fresh_posts],
    }

    return render(request, 'index.html', context)


def post_detail(request, slug):
    """Post page representation view"""
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            "text": comment.text,
            "published_at": comment.published_at,
            "author": comment.author.username,
        })
 
    serialized_post = {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments": serialized_comments,
        "likes_amount": post.likes.count(),
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
    }

    context = {
        "page_title": "Post page",
        "post": serialized_post,
    }
    return render(request, 'blog-details.html', context)


def contact(request):
    """Contact page representation view"""
    folium_map = folium.Map(location=COMPANY_COORDINATES, zoom_start=12)
    folium.Marker(
        COMPANY_COORDINATES,
        tooltip="Мы здесь",
    ).add_to(folium_map)
    html_map = folium_map._repr_html_()
    return render(request, 'contact.html', {"html_map": html_map})
