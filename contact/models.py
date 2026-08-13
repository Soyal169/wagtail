from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import render

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from .forms import ContactForm


class ContactSubmission(models.Model):
    """A record of every contact form submission, kept for reference alongside the email notification."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.created_at:%Y-%m-%d %H:%M}"


class ContactPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    intro_heading = models.CharField(max_length=160, default="Direct Contact Details")
    intro_text = RichTextField(
        default="<p>Reach out about roles, freelance projects, or technical collaboration.</p>",
        features=["bold", "italic", "link"],
    )
    success_message = models.CharField(
        max_length=200,
        default="Thank you! Your message has been sent — I'll get back to you shortly.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_heading"),
        FieldPanel("intro_text"),
        FieldPanel("success_message"),
    ]

    def serve(self, request, *args, **kwargs):
        feedback = None
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                ContactSubmission.objects.create(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                    subject=form.cleaned_data.get("subject", ""),
                    message=form.cleaned_data["message"],
                )
                send_mail(
                    subject=f"Portfolio contact: {form.cleaned_data.get('subject') or 'New message'}",
                    message=(
                        f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                        f"{form.cleaned_data['message']}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                    fail_silently=False,
                )
                feedback = {"type": "success", "text": self.success_message}
                form = ContactForm()
            else:
                feedback = {
                    "type": "error",
                    "text": "Please correct the errors below and try again.",
                }
        else:
            form = ContactForm()

        context = self.get_context(request)
        context["form"] = form
        context["feedback"] = feedback
        return render(request, self.get_template(request), context)
