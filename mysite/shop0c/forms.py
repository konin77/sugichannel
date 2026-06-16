from django import forms

class LoginForm(forms.Form):

    
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

    id = forms.CharField(label='会員ID', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード', max_length=256,widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))

class RegistUserForm(forms.Form):

    id = forms.CharField(label='会員ID：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード：', max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))
    password_confirm = forms.CharField(label='パスワード（確認）：', max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))
    name = forms.CharField(label='お名前：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(label='ご住所：', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('パスワードと確認用パスワードが一致しません')
        

class UpdateUserForm(forms.Form):

    password = forms.CharField(label='パスワード：', max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))
    password_confirm = forms.CharField(label='パスワード（確認）：', max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))
    name = forms.CharField(label='お名前：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(label='ご住所：', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('パスワードと確認用パスワードが一致しません')
        
    
'''
class Search(forms.Form):
    keyword = forms.CharField(label='キーワード：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
'''



