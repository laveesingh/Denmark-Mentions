from django import forms


class Form(forms.Form):
    keywords = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'enter your search keywords...'
                    }
                )
            )

