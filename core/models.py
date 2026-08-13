from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting(icon="cog")
class SiteBrandSettings(BaseSiteSetting):
    """Site-wide brand, contact, and structured-data defaults editable from the admin."""

    site_name = models.CharField(max_length=60, default="Soyal.dev")
    tagline = models.CharField(
        max_length=160,
        default="Senior Backend Developer & Software Engineer",
    )
    footer_blurb = models.TextField(
        default=(
            "Backend-focused software engineer building reliable APIs, "
            "CMS platforms, and data-driven systems."
        )
    )
    location = models.CharField(max_length=120, default="Kathmandu, Nepal")
    availability_status = models.CharField(
        max_length=160,
        default="Available for Senior Backend & Software Engineering Roles",
    )

    contact_email = models.EmailField(default="soyal@example.com")
    github_url = models.URLField(blank=True, default="https://github.com/")
    linkedin_url = models.URLField(blank=True, default="https://www.linkedin.com/")

    person_name = models.CharField(max_length=80, default="Soyal")
    person_job_title = models.CharField(
        max_length=160,
        default="Senior Backend Developer & Software Engineer",
    )
    knows_about = models.CharField(
        max_length=500,
        default=(
            "Python, Django, FastAPI, PHP, Laravel, Wagtail CMS, REST APIs, "
            "MySQL, PostgreSQL, Database Design, API Security"
        ),
        help_text="Comma-separated list used in the homepage Person JSON-LD.",
    )
    org_name = models.CharField(
        max_length=160, default="Soyal Engineering Portfolio"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("site_name"),
                FieldPanel("tagline"),
                FieldPanel("footer_blurb"),
                FieldPanel("location"),
                FieldPanel("availability_status"),
            ],
            heading="Brand",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_email"),
                FieldPanel("github_url"),
                FieldPanel("linkedin_url"),
            ],
            heading="Contact & social",
        ),
        MultiFieldPanel(
            [
                FieldPanel("person_name"),
                FieldPanel("person_job_title"),
                FieldPanel("knows_about"),
                FieldPanel("org_name"),
            ],
            heading="Structured data (SEO)",
        ),
    ]

    class Meta:
        verbose_name = "Site brand settings"
