# Create your views here.
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template import RequestContext
from MyBlogApp.blogfy import html_to_content
from models import Blog
from datetime import datetime


def show_list(request):
    blog_list = Blog.objects.all()
    return render_to_response("blogList.html",
                              {'blog_list': blog_list, 'modification': None},
                              context_instance=RequestContext(request)
    )


def edit_blog(request, blog_id):
    if Blog.exists(blog_id):
        blog = Blog.objects.get(id=int(blog_id))
        modification = 'edit'
    else:
        blog = Blog()
        blog.id = int(blog_id)
        blog.title = 'New blog'
        blog.time = datetime.now()
        modification = 'add'

    if request.method == "POST" and request.POST.has_key("content") and request.POST.has_key("title"):

        if request.session.get('edited_version'):
            edited_version = int(request.session.get('edited_version'))
        else:
            edited_version = -1 #Error

        content = html_to_content(request.POST["content"])
        if edited_version == blog.version:
            blog.content_body = content
            blog.title = request.POST["title"]
            blog.version += 1
            blog.save()
            return render_to_response("blogList.html",
                                      {'blog_list': Blog.objects.all(), 'modification': modification},
                                      context_instance=RequestContext(request))
        else:
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
    if Blog.exists(blog_id):
        blog = Blog.objects.get(id=int(blog_id))
    else:
        blog = None

    return render_to_response("displayblog.html",
                              {'blog': blog},
                              context_instance=RequestContext(request)
    )


def add_blog(request):
    blog = Blog()
    blog.title = 'New Blog'
    blog.content_body = ''
    blog.time = datetime.now()
    blog.save()

    return render_to_response("edit.html",
                              {'blog': blog},
                              context_instance=RequestContext(request)
    )


def delete_blog(request, blog_id):
    if Blog.exists(blog_id):
        blog = Blog.objects.get(id=int(blog_id))
        blog.delete()
        modification = "delete"
    else:
        modification = None

    return render_to_response("blogList.html",
                              {'blog_list': Blog.objects.all(), 'modification': modification},
                              context_instance=RequestContext(request))