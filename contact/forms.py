from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={"id": "form-name", "placeholder": "e.g. Alex Morgan"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"id": "form-email", "placeholder": "alex@company.com"}
        )
    )
    subject = forms.CharField(
        max_length=160,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "form-subject",
                "placeholder": "e.g. Senior Backend Role / Wagtail Migration",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "form-message",
                "rows": 5,
                "placeholder": "Tell me about your project, engineering requirements, or opportunity...",
            }
        )
    )
    # Honeypot field: real visitors never see or fill this in.
    company = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_company(self):
        if self.cleaned_data.get("company"):
            raise forms.ValidationError("Spam detected.")
        return self.cleaned_data["company"]
