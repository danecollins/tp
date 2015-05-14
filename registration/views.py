from __future__ import print_function
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render,render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from forms import UserForm



def newuser(request):
    if request.user.is_anonymous():
        form = UserForm(request.POST or None)
        if form.is_valid():
            form_data = form.save(commit=False)
            # if User.objects.filter(username=form_data.username) is None:
            u = User.objects.create_user(first_name=form_data.first_name,
                                         last_name=form_data.last_name,
                                         username=form_data.username,
                                         password=form_data.password,
                                         email=form_data.email)
            u.save()
            print('Created new user:{} with name {} {}'.format(form_data.username,
                                                        form_data.first_name,
                                                        form_data.last_name))
            user = authenticate(username=form_data.username,
                                password=form_data.password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/newuser.html', {'form': form})
    else:
        return render(request, 'registration/already_logged_on.html')
