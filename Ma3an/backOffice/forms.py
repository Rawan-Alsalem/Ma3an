from django import forms
from .models import Agency, Subscription

class AgencyApprovalForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['approved']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan', 'active', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }
