from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render,render_to_response, get_object_or_404
from django.template import RequestContext

from models import Post
from forms import PostForm, CommentForm


def can_post(user):
    return user.is_superuser or user.username == 'dane'


@user_passes_test(lambda u: can_post(u))
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render_to_response('blog/add_post.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(request.path)
    return render_to_response('blog/detail_view.html',
                              {'post': post, 'form': form},
                              context_instance=RequestContext(request))


def archive(request):
    posts = sorted(Post.objects.all(), key=lambda x: x.created_on, reverse=True)
    return render(request, 'blog/archive.html', {'posts': posts,
                                                 'show_add': can_post(request.user)})
