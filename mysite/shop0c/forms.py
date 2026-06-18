from django import forms
from .models import Category


class LoginForm(forms.Form):
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
    
class PurchaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    destination = forms.CharField(
        label="配送先",
        max_length=256
    )

    payment_method = forms.ChoiceField(
        label="支払方法",
        choices=(
            ("代引き", "代引き"),
        )
    )


class AdminLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    admin_id = forms.CharField(label="管理者ID", max_length=128, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(attrs={"class": "form-control"}))


class ItemRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    item_id = forms.IntegerField(label="商品ID", min_value=1)
    name = forms.CharField(label="商品名", max_length=128, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.ModelChoiceField(label="カテゴリ", queryset=Category.objects.all().order_by("category_id"), empty_label="選択してください")
    manufacturer = forms.CharField(label="メーカー名", max_length=32, widget=forms.TextInput(attrs={"class": "form-control"}))
    color = forms.CharField(label="商品の色", max_length=16, widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.IntegerField(label="価格", min_value=0)
    stock = forms.IntegerField(label="在庫数", min_value=0)
    recommended = forms.BooleanField(label="オススメ", required=False)
    # ★ 追加：商品画像（任意）
    image = forms.ImageField(label="商品画像", required=False)


class ItemUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    item_id = forms.IntegerField(label="商品ID", min_value=1)
    name = forms.CharField(label="商品名", max_length=128, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.ModelChoiceField(label="カテゴリ", queryset=Category.objects.all().order_by("category_id"), empty_label="選択してください")
    manufacturer = forms.CharField(label="メーカー名", max_length=32, widget=forms.TextInput(attrs={"class": "form-control"}))
    color = forms.CharField(label="商品の色", max_length=16, widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.IntegerField(label="価格", min_value=0)
    stock = forms.IntegerField(label="在庫数", min_value=0)
    recommended = forms.BooleanField(label="オススメ", required=False)
    # ★ 追加：商品画像（任意・空のままで変更しない）
    image = forms.ImageField(label="商品画像", required=False)


class AdminPurchaseHistorySearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    purchase_id = forms.IntegerField(
        label="注文ID",
        required=False,
        min_value=1
    )

    user_id = forms.CharField(
        label="会員ID",
        required=False,
        max_length=128
    )

    item_name = forms.CharField(
        label="商品名",
        required=False,
        max_length=128
    )

    cancel = forms.ChoiceField(
        label="キャンセル状態",
        required=False,
        choices=[
            ("all", "すべて"),
            ("not_cancel", "未キャンセル"),
            ("cancel", "キャンセル済み"),
        ]
    )