from django import forms
from .models import User
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    city=forms.CharField(required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'city')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    # username = forms.CharField(label='Username', validators=[
    #     RegexValidator(
    #         regex=USERNAME_REGEX,
    #         message='Username must be alphanumeric',
    #         code='invalid_username'
    #         )])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    ### FOR ERROR MESSAGE METHOD 1
    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     the_user = user = authenticate(username=email, password=password)
    #     if not the_user:
    #         raise forms.ValidationError("Invalid Credentials!!!")

    ### FOR ERROR MESSAGE METHOD 2
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            raise forms.ValidationError("Invalid Credentials!! [USERNAME]")
        if not user_obj.check_password(password):
                # log auth tries
            raise forms.ValidationError("Invalid Credentials!! [PASSWORD]")
        if not user_obj.is_active:
            raise forms.ValidationError("User is Inactive. Please check your email!")

        return super(UserLoginForm, self).clean(*args, **kwargs)
