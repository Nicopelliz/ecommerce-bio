from django import forms

PAYMENT_OPTIONS = (
    ('S','Stripe'),
    ('P','PayPal')
)


class CheckoutForm(forms.Form):
    indirizzo = forms.CharField(max_length=200, widget= forms.TextInput(attrs={'class': 'form-control col-md-12',
                                                                               'placeholder': 'Via/Piazza...',
                                                                               'type': "text"}))
    citta = forms.CharField(max_length=200)
    provincia = forms.CharField(max_length=3)
    codice_postale = forms.CharField()
    usa_come_indirizzo_di_fatturazione = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    salva = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    opzioni_di_pagamento = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=PAYMENT_OPTIONS)