from django.shortcuts import redirect
from blog.forms import CommentForm

from django.utils import timezone
from django.shortcuts import render

from .models import Post

# Create your views here.
def index(request):
  posts = Post.objects.filter(published_at__lte=timezone.now())
  
  if request.user.is_active:
    if request.method == "POST":
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()
        return redirect(request.path_info)
    else:
      comment_form = CommentForm()
  else:
    comment_form = None

  
  return render(request, "blog/index.html", {"post" : post, "comment_form": comment_form})
  