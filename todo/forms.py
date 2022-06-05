from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from .models import Todo
from django.utils.translation import gettext_lazy as _


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']


class ModifyUserCreationForm(UserCreationForm):
    """DOCSTRING: add email and correct validation of password field to default UserCreationForm"""
    error_css_class = 'error'
    required_css_class = 'required'
    email = forms.EmailField(required=True,)

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
        "error_for_firstpass": _("The two password fields didn’t match1."),
    }

    class Meta:
        model = User
        fields = ('username', 'email')
        help_texts = {
            'email': _('E-mail'),
        }

    def clean_email(self):
        value = self.cleaned_data.get('email')
        if User.objects.filter(email=value).exists():
            raise ValidationError((f"{value} is taken."), params={'value': value})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password1','')
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        ModelForm._post_clean(self)
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1','')
                self.add_error('password2', error)