from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

import json
from django.core import serializers

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail

# Help function to guess a MIME type from a file name
from mimetypes import  guess_type

from grumblr.models import *
from grumblr.forms import *

# Global Stream here
@login_required
def home(request):
    context=dict()
	# Set up a list of all the items of the newly logged-in user
    # posts = Post.objects.all().order_by('-time')
    # context['posts'] = posts
    #
    # post_users = list()
    # for post in posts:
     #    user_info = get_object_or_404(UserInfo, user = post.user)
     #    post_users.append(user_info)
    # context['post_users'] = post_users

    # context['form'] = PostForm()
    # user_info = get_object_or_404(UserInfo, user = request.user)
    # context['firstname'] = user_info.firstname
    # context['lastname'] = user_info.lastname
    #
    # comments = Comment.objects.all().order_by('time')
    # context['comments'] = comments

    return render(request, 'grumblr/global_stream.html', context)

# follower stream
@login_required
def follower(request, username):
    context = dict()
    # Get the current user
    follower = get_object_or_404(UserInfo, user = request.user)
    posts = Post.objects.filter(user__in = follower.followee.all()).order_by('-time')
    context['posts'] = posts
    user_info = get_object_or_404(UserInfo, user=request.user)
    context['firstname'] = user_info.firstname
    context['lastname'] = user_info.lastname

    comments = Comment.objects.all().order_by('time')
    context['comments'] = comments

    return render(request, 'grumblr/follow_stream.html', context)

@login_required
def follow(request, username):
    context = dict()
    # User that current user intend to follow
    user = User.objects.get(username = username)
    if not user:
        raise Http404
    # Current user
    follower = get_object_or_404(UserInfo, user = request.user)
    # Follow the user
    if not user in list(follower.followee.all()):
        # context['follow'] = 'follow'
        follower.followee.add(user)
    else:
        # Unfollow the user
        # context['unfollow'] = 'unfollow'
        follower.followee.remove(user)
    follower.save()
    url = '/grumblr/profile/' + user.username
    return redirect(url)

@login_required
def profile(request, username):
    context = dict()
    # User that clicked to view its profile or follow and unfollow
    try:
        click_user = User.objects.get(username = username)
    except User.DoesNotExist:
        raise Http404("No model matches the given query.")

    context['email'] = click_user.email

    # make all posts in reverse chronological mode
    posts = Post.objects.filter(user = click_user).order_by('-time')
    # Get user_info object
    user_info = get_object_or_404(UserInfo, user = click_user)

    context['age'] = user_info.age
    context['bio'] = user_info.bio
    context['firstname'] = user_info.firstname
    context['lastname'] = user_info.lastname
    context['click_user'] = click_user

    # Current user
    follower = get_object_or_404(UserInfo, user = request.user)
    # Following State
    if not click_user in list(follower.followee.all()):
        context['follow'] = False
    else:
        # Unfollow the user
        context['follow'] = True
    context['posts'] = posts
    return render(request, 'grumblr/profile.html', context)

# Upload image here edit the profile
@login_required
def edit_entry(request, username):
    context = dict()
    entry_to_edit = get_object_or_404(UserInfo, user=request.user)
    context['firstname'] = entry_to_edit.firstname
    context['lastname'] = entry_to_edit.lastname

    if request.method == "GET":
        form = UserInfoForm(instance = entry_to_edit)
        context['form'] = form
        return render(request, 'grumblr/edit_profile.html', context)

    form = UserInfoForm(request.POST, request.FILES, instance = entry_to_edit)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'grumblr/edit_profile.html', context)
    form.save()

    url = '/grumblr/profile/' + request.user.username
    return redirect(url)

@login_required
def get_photo(request, username):
    click_user = User.objects.get(username = username)
    user = get_object_or_404(UserInfo, user = click_user)
    if not user.picture:
        raise Http404
    # content_type = guess_type(img.picture.name)
    return HttpResponse(user.picture)

# Add post
@login_required
def add_item(request):
    errors = []
    if not 'item' in request.POST or not request.POST['item']:
        errors.append('You must enter an post to add.')
    else:
        new_post = Post(user = request.user, text = request.POST['item'])
        new_post.save()
    return redirect(reverse('home'))

@login_required
def delete_item(request, id):
    errors = []
    # Deletes item if the logged-in user has an item matching the id
    try:
        item_to_delete = Post.objects.get(id=id, user=request.user)
        # item_to_delete.delete()
        item_to_delete.deleted = True
    except ObjectDoesNotExist:
        errors.append('The item did not exist in your todo list.')
    url = '/grumblr/profile/' + request.user.username
    return redirect(url)

@login_required
def update_posts(request):
    response_text = dict()
    posts = Post.objects.all()
    users = User.objects.all()
    user_info = UserInfo.objects.all()
    response_text['posts_json'] = serializers.serialize('json', posts)
    response_text['users_json'] = serializers.serialize('json', users)
    response_text['info_json'] = serializers.serialize('json', user_info)
    return HttpResponse(json.dumps(response_text), content_type = 'application/json')

@login_required
@transaction.atomic
def add_comment(request, id):
    errors = []
    context = dict()
    if not 'comment' in request.POST or not request.POST['comment']:
        errors.append('You must enter an comment to add.')
    # if request.method == "GET":
    #     return render(request, 'grumblr/global_stream.html', context)
    else:
        post = Post.objects.get(id = id)
        new_comment = Comment(text = request.POST['comment'], post = post, user = request.user)
        new_comment.save()
    return redirect(reverse('home'))

def send_email(request, username):
    context = dict()
    user = User.objects.get(username = username)
    new_user = get_object_or_404(UserInfo, user = user)
    token = default_token_generator.make_token(user)
    new_user.token = token
    new_user.save()
    content = """
    Welcome to Grumblr. Please click the link below to activate your account
    """
    url = 'http://%s%s'% (request.get_host(), reverse('confirm', args=(user.username, token)))
    email_body = content + url
    send_mail(subject = "Verify your email address",
              message = email_body,
              from_email = "chengqij@andrew.cmu.edu",
              recipient_list = [user.email])
    context['message'] = """Check you mail box to activate your account"""
    return render(request, 'grumblr/confirmation.html', context)

def change_request(request, username):
    context = dict()
    user = User.objects.get(username=username)
    new_user = get_object_or_404(UserInfo, user=user)
    token = default_token_generator.make_token(user)
    new_user.token = token
    new_user.save()
    content = """
        Check your password via the link below
        """
    url = 'http://%s%s' % (request.get_host(), reverse('change', args=(user.username, token)))
    email_body = content + url
    send_mail(subject="Change your password",
              message=email_body,
              from_email="chengqij@andrew.cmu.edu",
              recipient_list=[user.email])
    context['message'] = """An email has been sent to your mail box to reset your password"""
    return render(request, 'grumblr/change_password.html', context)

def change_permit(request,username, token):
    user = User.objects.get(username = username)
    new_user = get_object_or_404(UserInfo, user=user)
    if new_user.token != token:
        raise Http404
    else:
        return redirect(reverse('password'))

@transaction.atomic
def confirm_change(request):
    context = dict()
    # Get UserInfo
    new_user = get_object_or_404(UserInfo, user = request.user)
    if request.method == 'GET':
        context['form'] = PasswordForm()
        return render(request, 'grumblr/password.html', context)
    form = PasswordForm(request.POST, instance = new_user)
    if not form.is_valid():
        return render(request, 'grumblr/password.html', context)

    form.save()
    if request.user.password != form.cleaned_data['password'] and form.cleaned_data['password'] != '':
        request.user.set_password(form.cleaned_data['password'])
        request.user.save()
    return redirect('/grumblr/login')

def confirm_registration(request, username, token):
    # Get UserInfo
    user = User.objects.get(username = username)
    new_user = get_object_or_404(UserInfo, user = user)
    # login(request, user)
    if new_user.token != token:
        raise Http404
        # new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
    user.is_active = True
    user.save()
    # login_user = authenticate(username = user.username, password = user.password)
    # login(request, login_user)
    return redirect('/grumblr/')

def register(request):
    context = dict()
    #Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/register.html',context)

    # Creates a bound form from the request POST parameters and makes the form
    # available in the request context dictionary
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validate the form
    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'],
    first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'])
    new_user.is_active = False
    new_user.save()

    # Create user info form
    new_info = UserInfo(user = new_user)
    info_form = UserInfoForm(request.POST, instance = new_info)
    info_form.save()

    # Logs in the new user and redirect
    # new_user = authenticate(username=request.POST['username'], password = request.POST['password1'])
    # login(request, new_user)
    url = '/grumblr/confirmation/' + new_user.username
    return redirect(url)

# Returns all recent additions in the database, as JSON
def get_items(request, time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    items = Post.get_items(time)
    context = {"max_time": max_time, "items": items}
    return render(request, 'grumblr/items.json', context, content_type='application/json')

# Returns all recent changes to the database, as JSON
def get_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    items = Post.get_changes(time)
    context = {"max_time": max_time, "items": items}
    return render(request, 'grumblr/items.json', context, content_type='application/json')

# Return all recent comments in database
def get_comments(request, id, time="1970-01-01T00:00+00:00"):
    # if time == "undefined":
    #     time = "1970-01-01T00:00+00:00"
    max_time = Comment.get_max_time()
    comments = Comment.get_comments(id, time)
    context = {"max_time": max_time, "comments": comments}
    return render(request, 'grumblr/comments.json', context, content_type='application/json')

def get_comment_changes(request, id, time="1970-01-01T00:00+00:00"):
    # if time == "undefined":
    #     time = "1970-01-01T00:00+00:00"
    max_time = Comment.get_max_time()
    comments = Comment.get_changes(id, time)
    context = {"max_time": max_time, "comments": comments}
    return render(request, 'grumblr/comments.json', context, content_type='application/json')

def get_follow_items(request, username, time="1970-01-01T00:00+00:00"):
    user = User.objects.get(username = username)
    new_user = get_object_or_404(UserInfo, user = user)
    max_time = Post.get_max_time()
    items = Post.objects.filter(user__in = new_user.followee.all())
    context = {"max_time": max_time, "items": items}
    return render(request, 'grumblr/items.json', context, content_type = 'application/json')

def get_profile_items(request, username, time="1970-01-01T00:00+00:00"):
    user = User.objects.get(username=username)
    max_time = Post.get_max_time()
    items = Post.objects.filter(user = user)
    context = {"max_time": max_time, "items": items}
    return render(request, 'grumblr/items.json', context, content_type='application/json')


