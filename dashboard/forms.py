from django import forms


class DateForm(forms.Form):
    date_init = forms.CharField(label="between: ", widget=forms.TextInput(attrs={
        'placeholder': 'date',
        'type': 'date'}))
    date_fin = forms.CharField(label="and:", widget=forms.TextInput(attrs={
        'placeholder': 'date',
        'type': 'date'}))
class SearchForm(forms.Form):
    ref_no = forms.CharField(max_length=255,widget=forms. TextInput({ "placeholder": "Reference No"}))
    account= forms.CharField(max_length=255,widget=forms. TextInput({ "placeholder": "Account No"}))
    amount = forms.CharField(max_length=255,widget=forms. TextInput({ "placeholder": "Amount"}))
class SearchType(forms.Form):
    type = forms.CharField(widget=forms.Select(choices=(('Search By Date','Search By Date'),('Search By Field','Search By Field'))))