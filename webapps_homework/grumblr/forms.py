from django import forms

from django.contrib.auth.models import User
from grumblr.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    email = forms.EmailField(max_length = 40)
    firstname = forms.CharField(max_length = 40)
    lastname = forms.CharField(max_length = 40)
    password1 = forms.CharField(max_length = 40, label = 'Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 40, label = 'ConfirmPassword',
                                widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more than one field.
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        # confirm that the two passwords fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match")
        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    # Customize form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already in the User model database
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact = username):
            raise forms.ValidationError("Username is already taken")
        # Generally return the cleaned data we got from the cleaned data
        return username

class PostForm(forms.ModelForm):
    # age = forms.CharField(max_length=20)
    class Meta:
        model = Post
        exclude = ('user', )
        widgets = {
            'post': forms.TextInput()
        }

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        exclude = ('user', 'followee', 'password', 'token')
        widgets = {
            'picture': forms.FileInput(),
            'age': forms.TextInput(),
            'bio': forms.TextInput(),
            'firstname': forms.TextInput(),
            'lastname': forms.TextInput()
        }

class PasswordForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        exclude = ('user', 'followee', 'token', 'picture', 'age', 'bio', 'firstname', 'lastname')
        widgets = {
            'password': forms.TextInput()
        }
