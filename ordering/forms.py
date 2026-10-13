from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "table_number", "phone", "notes"]
        labels = {
            "customer_name": "Your name",
            "table_number": "Table number",
            "phone": "Phone (optional)",
            "notes": "Notes for the kitchen (optional)",
        }
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "table_number": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 99, "inputmode": "numeric"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel", "inputmode": "tel"}),
            "notes": forms.TextInput(attrs={"class": "form-control", "placeholder": "Less spicy, no onions..."}),
        }

    def clean_customer_name(self):
        name = self.cleaned_data["customer_name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your name.")
        return name


class TrackForm(forms.Form):
    order_id = forms.IntegerField(
        min_value=1,
        max_value=2_000_000_000,
        label="Order ID",
        widget=forms.NumberInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "e.g. 12", "inputmode": "numeric"}
        ),
    )


class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES)
