# Create your views here.
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from blogfy import html_to_content
from models import Blog
from datetime import datetime


def init_session_data(request):
    if not request.session.get('session_start_time'):
        request.session['session_start_time'] = datetime.now().strftime('%a %d, %Y, %I:%M %p')

    if not request.session.get('articles_edited'):
        request.session['articles_edited'] = []

    if not request.session.get('articles_visited'):
        request.session['articles_visited'] = []

    if not request.session.get('articles_created'):
        request.session['articles_created'] = []

    if not request.session.get('articles_deleted'):
        request.session['articles_deleted'] = []

    if not request.session.get('modification'):
        request.session['modification'] = None

    if not request.session.get('blog_modified'):
        request.session['blog_modified'] = None


def show_list(request):
    init_session_data(request)
    blog_list = Blog.objects.all()
    modification = request.session['modification']
    request.session['modification'] = None
    message = request.session.get("message_to_home")
    request.session["message_to_home"] = None

    return render_to_response("blogList.html",
                              {'blog_list': blog_list,
                               'modification': modification,
                               'blog_modified': request.session['blog_modified'],
                               'session_start_time': request.session.get('session_start_time'),
                               'articles_edited': len(request.session.get('articles_edited')),
                               'articles_visited': len(request.session.get('articles_visited')),
                               'articles_deleted': len(request.session.get('articles_deleted')),
                               'articles_created': len(request.session.get('articles_created')),
                               'user': request.user,
                               'message': message
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def edit_blog(request, blog_id):
    init_session_data(request)
    if Blog.exists(blog_id):
        blog = Blog.objects.get(id=int(blog_id))
    else:
        return add_blog(request, int(blog_id))

    request.session['blog_modified'] = blog.id

    if request.method == "POST" and request.POST.has_key("content") and request.POST.has_key("title"):

        if request.session.get('edited_version'):
            edited_version = int(request.session.get('edited_version'))
        else:
            edited_version = -1

        content = html_to_content(request.POST["content"])
        if edited_version == blog.version:
            blog.content_body = content
            blog.title = request.POST["title"]
            blog.version += 1
            blog.save()
            if request.session['modification'] != 'add':
                request.session['modification'] = 'edit'
                request.session['articles_edited'] = request.session['articles_edited'].append(blog_id)
            return HttpResponseRedirect('/myblog/')

        else:
            request.session['edited_version'] = str(blog.version)
            return render_to_response("conflict.html",
                                      {'blog': blog, 'user_content': content},
                                      context_instance=RequestContext(request)
            )
    request.session['edited_version'] = str(blog.version)
    return render_to_response("edit.html",
                              {'blog': blog},
                              context_instance=RequestContext(request)
    )


def display_blog(request, blog_id):
    init_session_data(request)
    if Blog.exists(blog_id):
        blog = Blog.objects.get(id=int(blog_id))
        request.session['articles_visited'].append(blog_id)
    else:
        blog = None

    return render_to_response("displayblog.html",
                              {'blog': blog},
                              context_instance=RequestContext(request)
    )


@login_required
def add_blog(request, blog_id=None):
    init_session_data(request)
    blog = Blog()
    if blog_id:
        blog.id = blog_id
    blog.title = 'New Blog'
    blog.content_body = ''
    blog.time = datetime.now()
    blog.save()
    request.session['articles_created'] = request.session['articles_created'].append(blog.id)
    request.session['edited_version'] = str(blog.version)
    request.session['blog_modified'] = str(blog.id)
    request.session['modification'] = 'add'

    return HttpResponseRedirect('/editblog/' + str(blog.id))


@login_required
def delete_blog(request, blog_id):
    init_session_data(request)
    if Blog.exists(blog_id):
        blog = Blog.objects.get(id=int(blog_id))
        request.session['blog_modified'] = str(blog.id)
        blog.delete()
        request.session['modification'] = "delete"
        request.session['articles_deleted'] = request.session['articles_deleted'] | {blog_id}
    else:
        request.session['modification'] = None

    return HttpResponseRedirect('/myblog/')


def clear_session(request):
    if request.method == "POST" and request.POST.has_key("clearsession"):
        request.session.clear()

    return HttpResponseRedirect('/myblog/')


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session["message_to_home"] = "New User is created. Please Login"
            return HttpResponseRedirect("/myblog/")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {'form': form}, context_instance=RequestContext(request))


def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_to = request.GET.get('next', '/myblog/')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next_to)

    return render_to_response("log_in.html", {'error': "Please sign in"}, context_instance=RequestContext(request))


def log_out(request):
    logout(request)
    request.session["message_to_home"] = "Your are now logged out !!!"
    return HttpResponseRedirect("/myblog/")