from django import forms


class KeyForm(forms.Form):
    key_word = forms.CharField(label="key_word", max_length=100)
    genre = forms.CharField(label="genre", max_length=100)