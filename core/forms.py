from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your name",
                    "aria-label": "Your name",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your email",
                    "aria-label": "Your email",
                    "autocomplete": "email",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your message",
                    "aria-label": "Your message",
                    "rows": 5,
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your name.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < 5:
            raise forms.ValidationError("Please write a slightly longer message.")
        return message