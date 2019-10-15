from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, UserProfile, Address_details


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =('first_name',
                 'last_name',
                 'phone',
#                 'credit_card',
#                 'credit_card_type_id',
#                 'card_exp_month', 
#                 'card_exp_year', 
#                 'billing_address', 
#                 'billing_city', 
#                 'billing_state',
#                 'billing_pincode',    
#                 'billing_country', 
#                 'shipping_address', 
#                 'shipping_city', 
#                 'shipping_state', 
#                 'shipping_pincode',  
#                 'shipping_country', 
#                 'date_entered', 
            )
class ChangePassword(forms.Form):
    password=forms.CharField(label='Old Password',widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class ForgotPassword(forms.Form):    
    email=forms.CharField(label='Email', widget=forms.EmailInput)
    password1 = forms.CharField(label='New Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class Address_detailsForm(forms.ModelForm):
    class Meta:
        model = Address_details
        fields = ('name','house_no', 'building_name', 'landmark', 'city','state','pincode', 'country', 'phone')

class User_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(User_form, self).__init__(*args, **kwargs)
       self.fields['email'].widget.attrs['readonly'] = True
    class Meta:
        model = User
        fields = ('email',)

