from django import forms
from django.contrib.auth.models import User

# Using existing code from Project 1

class JoinForm(forms.ModelForm):
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class':'form-control',
				'autocomplete':'new-password'
			}
		)
	)

	class Meta():
		model = User
		fields = (
			'first_name',
			'last_name',
			'username',
			'email',
			'password'
		)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                'class':'form-control ml-2'
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class':'form-control ml-2'
            }
        )
    )
