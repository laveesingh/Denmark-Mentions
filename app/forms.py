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
    date = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'input-group-addon',
                    'placeholder': 'start date: dd-mm-yyyy',
                    'title': 'only results after date will be displayed',
                    'id': 'date'
                    }
                )
            )

