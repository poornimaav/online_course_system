from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User, Course, Content, Teacher

class LoginForm(forms.Form):
   
    email = forms.EmailField(
        widget= forms.EmailInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )

    password = forms.CharField(
        widget= forms.PasswordInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(
        widget= forms.TextInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )

    last_name = forms.CharField (
        widget= forms.TextInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )

    username=forms.CharField(
         widget= forms.TextInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )

    password1 = forms.CharField(
        widget= forms.PasswordInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )

    password2 = forms.CharField(
        widget= forms.PasswordInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )

    email = forms.EmailField(
        widget= forms.EmailInput(
           attrs= {
            'class': 'form-control'
           } 
        )
    )


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_teacher', 'is_student')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is Already registered")
        else:
            return email

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    bio = forms.CharField(max_length=500, required=True)
    expertise = forms.CharField(max_length=100, required=True)
    is_teacher = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'bio', 'expertise', 'is_teacher' ,'password1', 'password2')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError('First name should contain only alphabets.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('Last name should contain only alphabets.')
        return last_name


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    # major = forms.CharField(max_length=50, required=False)
    # university = forms.CharField(max_length=100, required=False)
    # degree = forms.CharField(max_length=30, required=False)
    is_student = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_student', 'password1', 'password2',)
  
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields=['title', 'description', 'duration','price']
        widgets={
            'description' : forms.Textarea(
                attrs={'rows':5},
            )
        }

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'text', 'video_url']


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email address is not registered, please enter an valid email")
        return email