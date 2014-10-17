from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from MyBlogApp.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyBlog.views.home', name='home'),

    url(r'^myblog/$', show_list),

    url(r'^editblog/(?P<blog_id>\w+)/$', edit_blog),

    url(r'^myblog/(?P<blog_id>\w+)/$', display_blog),

    url(r'^deleteblog/(?P<blog_id>\w+)/$', delete_blog),

    url(r'^addblog/$', add_blog),

    url(r'^clearsession/$', clear_session),

    url(r'^createuser/$', create_user),

    url(r'^login/$', log_in),

    url(r'^logout/$', log_out),



    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
