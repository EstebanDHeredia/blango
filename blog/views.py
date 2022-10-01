from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


import logging
from django.shortcuts import redirect
from blog.forms import CommentForm

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import render

from .models import Post

logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
  posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
  logger.debug("Got %d posts", len(posts))
  return render(request, "blog/index.html", {"posts" : posts})

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)

  if request.user.is_active:
    if request.method == "POST":

      
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()
        logger.info("Created comment on Post %d for user %s", post.pk, request.user)
        return redirect(request.path_info)
    else:
      comment_form = CommentForm()
  else:
    comment_form = None

  return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])
