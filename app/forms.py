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
                ),
            required=False
            )
    ids = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'IDs',
                    'title': 'space separated ids to limit results',
                    'id': 'ids'
                    }
                ),
            required=False
            )
    export_to_excel = forms.BooleanField(
            widget=forms.CheckboxInput(
                attrs={
                    'class': 'input-group-addon',
                    'title': 'check this box if you want to download results',
                    }
                ),
            required=False
            )
