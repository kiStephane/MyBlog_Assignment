from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyBlog.views.home', name='home'),

    url(r'^myblog/$', 'MyBlogApp.views.show_list'),

    url(r'^editblog/(?P<blog_id>\w+)/$', 'MyBlogApp.views.edit_blog'),

    url(r'^myblog/(?P<blog_id>\w+)/$', 'MyBlogApp.views.display_blog'),

    url(r'^deleteblog/(?P<blog_id>\w+)/$', 'MyBlogApp.views.delete_blog'),

    url(r'^addblog/$', 'MyBlogApp.views.add_blog'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
