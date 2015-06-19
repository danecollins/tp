from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['id', 'author', 'slug']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
