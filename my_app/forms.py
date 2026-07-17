from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Post


class UserRegistrationForm(UserCreationForm): #inheritance
    class Meta:
       model = User
       fields = ['username','email','password1','password2']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','subtitle','image','content']
