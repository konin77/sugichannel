from django import forms

class LoginForm(forms.Form):

    
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

    id = forms.CharField(label='会員ID：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード：', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))

class RegistUserForm(forms.Form):

    id = forms.CharField(label='会員ID：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード：', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))
    password_confirm = forms.CharField(label='パスワード（確認）：', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='お名前：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(label='ご住所：', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))

'''
class Search(forms.Form):
    keyword = forms.CharField(label='キーワード：', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
'''



