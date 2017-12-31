from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=255, strip=True, label='', label_suffix='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Логин',
            'autofocus': 'autofocus',
        })
    )

    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
    }), label='', label_suffix='')
