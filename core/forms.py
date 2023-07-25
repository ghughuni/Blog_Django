from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body', 'slug']			

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("This user is not active")

		return super(UserLoginForm, self).clean(*args, **kwargs)
	
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
	
	