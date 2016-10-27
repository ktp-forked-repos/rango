from django import forms
from django.contrib.auth.models import User
from cms2d.models import Topic


class TopicForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter a topic name")
    author_id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Topic
        fields = ('name', 'author_id')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
