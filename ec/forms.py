from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



from .models import Contact, CustomUser, Comment


        
class ContactForm(forms.ModelForm):
    name = forms.CharField(label="氏名")
    email = forms.EmailField(label="メールアドレス", widget=forms.EmailInput())
    subject = forms.CharField(label="件名")
    text = forms.CharField(label="本文", widget=forms.Textarea)
    
    def __init__(self, *arg, **kwargs):
        super(ContactForm, self).__init__(*arg, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'text')
        
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザーID')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    def __init__(self, *arg, **kwargs):
        super(LoginForm, self).__init__(*arg, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        

class UserCreateForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーID')
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='パスワード（確認）', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = CustomUser
        fields = ('username','password1', 'password2' )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
        
        
class AccountForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーID')
    email = forms.EmailField(widget=forms.EmailInput(), label='メールアドレス')
    last_name = forms.CharField(required=False, label='姓')
    first_name = forms.CharField(required=False, label='名')
    
    def __init__(self, *arg, **kwargs):
        super(AccountForm, self).__init__(*arg, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name')
        
        
class CommentForm(forms.ModelForm):
    author = forms.CharField(label='投稿者')
    text = forms.CharField(label='本文', widget=forms.Textarea)
    
    def __init__(self, *arg, **kwargs):
        super(CommentForm, self).__init__(*arg, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Comment
        fields = ('author', 'text')