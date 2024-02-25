from .models import Users
from django import forms


class UserSignUpForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=50,
                               widget=forms.widgets.TextInput(
                                   attrs={
                                       "placeholder": "Enter Full Name",
                                       "class": "form-control ",
                                   }
                               ), label="Full Name")
    email = forms.EmailField(required=True,
                             widget=forms.widgets.EmailInput(
                                 attrs={
                                     "placeholder": "Enter Email",
                                     "class": "form-control ",
                                 }
                             ), label="Email")

    phone = forms.CharField(required=True, max_length=10,
                            widget=forms.widgets.TextInput(
                                attrs={
                                    "placeholder": "Enter Phone Number",
                                    "class": "form-control ",
                                }
                            ), label="Phone Number")

    password = forms.CharField(required=True, max_length=15,
                               widget=forms.widgets.PasswordInput(
                                   attrs={
                                       "placeholder": "Enter Password",
                                       "class": "form-control",
                                   }
                               ), label="Password")

    class Meta:
        model = Users
        exclude = ["created_at", "updated_at", "is_active"]
        fields = ["username", "email", "phone", "password", ]
        widgets = {
            "password": forms.PasswordInput(),
        }


class AdminUserManagementForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = ["created_on", "updated_on"]
