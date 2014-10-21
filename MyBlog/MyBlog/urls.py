# Uncomment the next two lines to enable the admin:
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MyBlog.views.home', name='home'),

                       url(r'^myblog/$', 'MyBlogApp.views.show_list', name='show_list'),

                       url(r'^editblog/(?P<blog_id>\w+)/$', 'MyBlogApp.views.edit_blog', name='edit_blog'),

                       url(r'^myblog/(?P<blog_id>\w+)/$', 'MyBlogApp.views.display_blog', name='display_blog'),

                       url(r'^deleteblog/(?P<blog_id>\w+)/$','MyBlogApp.views.delete_blog', name='delete_blog' ),

                       url(r'^addblog/$','MyBlogApp.views.add_blog', name='add_blog'  ),

                       url(r'^clearsession/$','MyBlogApp.views.clear_session', name='clear_session' ),

                       url(r'^createuser/$', "MyBlogApp.views.create_user", name='create_user' ),

                       url(r'^login/$', 'MyBlogApp.views.log_in', name='log_in'),

                       url(r'^logout/$', 'MyBlogApp.views.log_out', name='log_out'),

                       url(r'^api/v1/blogs/$', 'MyBlogApp.rest_views.blog_create', name='blog_create'),


                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)
