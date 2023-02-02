from django import template
from postsapp.models import Post
register=template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()
@register.inclusion_tag('postsapp/latest_posts.html')
def showlatestposts(count=5):
    lat_posts=Post.objects.order_by('-publish')[:count]
    return {'latp':lat_posts}
