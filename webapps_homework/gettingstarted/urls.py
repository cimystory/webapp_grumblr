from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import grumblr.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^grumblr/', include('grumblr.urls')),
    url(r'^$', grumblr.views.home),
    # url(r'^db', hello.views.db, name='db'),
    # url(r'^admin/', include(admin.site.urls)),
]
