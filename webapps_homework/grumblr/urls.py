from django.conf.urls import include, url

import django.contrib.auth.views
import grumblr.views

urlpatterns = [
    url(r'^$', grumblr.views.home, name = 'home'),
    url(r'^add-item', grumblr.views.add_item, name = 'add'),
    url(r'^delete-item/(?P<item_id>\d+)$', grumblr.views.delete_item),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'grumblr/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', grumblr.views.register),
    url(r'^profile/(?P<username>\w+)$', grumblr.views.profile, name = 'profile'),
    url(r'^edit-entry/(?P<username>\w+)$', grumblr.views.edit_entry, name = 'edit'),
    url(r'^photo/(?P<username>\w+)$', grumblr.views.get_photo, name = 'photo'),
    # Route to follower stream
    url(r'^follower/(?P<username>\w+)$', grumblr.views.follower, name = 'follower'),
    url(r'^follow/(?P<username>\w+)$', grumblr.views.follow),
    # Route to send confirmation email
    url(r'^confirmation/(?P<username>\w+)$', grumblr.views.send_email, name = 'send'),
    url(r'^confirm/(?P<username>\w+)/(?P<token>\w.*)$', grumblr.views.confirm_registration, name = 'confirm'),
    # Route to change password
    url(r'^change/(?P<username>\w+)$', grumblr.views.change_request),
    url(r'^change/(?P<username>\w+)/(?P<token>\w.*)$', grumblr.views.change_permit, name = 'change'),
    url(r'^password$', grumblr.views.confirm_change, name = 'password'),
    # Route to add comments
    url(r'^add-comment/(?P<id>\d+)$', grumblr.views.add_comment, name = 'comment'),
    url(r'^get-comments/(?P<id>\d+)$', grumblr.views.get_comments),
    url(r'^get-comments/(?P<time>.+)$', grumblr.views.get_comments),
    url(r'^get-comment-changes/?$', grumblr.views.get_comment_changes),
    url(r'^get-comment-changes/(?P<id>\d+)/(?P<time>.+)$', grumblr.views.get_comment_changes),
    url(r'^get-profile-items/(?P<username>\w+)$', grumblr.views.get_profile_items),
    url(r'^get-follow-items/(?P<username>\w+)$', grumblr.views.get_follow_items),
    # Route to add posts
    url(r'^update-post', grumblr.views.update_posts),
    url(r'^get-items/?$', grumblr.views.get_items),
    url(r'^get-items/(?P<time>.+)$', grumblr.views.get_items),
    url(r'^get-changes/?$', grumblr.views.get_changes),
    url(r'^get-changes/(?P<time>.+)$', grumblr.views.get_changes),

]