from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.template import RequestContext

from models import Post, Comment
from forms import PostForm, CommentForm
import sys

def can_post(user):
    return user.is_superuser or user.username == 'dane'


@user_passes_test(lambda u: can_post(u))
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.id = None
        post.author = request.user
        post.save()
        return redirect('/blog/archive')
    return render(request, 'blog/add_post.html', {'form': form})


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        print('Comment added to blog post')
        return redirect(request.path)
    return render_to_response('blog/detail_view.html',
                              {'post': post, 'form': form},
                              context_instance=RequestContext(request))


def archive(request):
    posts = sorted(Post.objects.all(), key=lambda x: x.created_on, reverse=True)
    comments = Comment.objects.all()
    comment_info = {}
    for p in posts:
        comment_info[p.id] = dict(num_comments=0, last=p.created_on, post=p)
    for c in comments:
        comment_info[c.post.id]['num_comments'] += 1
        if c.created_on > comment_info[c.post.id]['last']:
            comment_info[c.post.id]['last'] = c.created_on

    pinfo = []
    for p in posts:
        pinfo.append(comment_info[p.id])

    print(comment_info, sys.stderr)
    return render(request, 'blog/archive.html', {'pinfo': pinfo,
                                                 'show_add': can_post(request.user)})
