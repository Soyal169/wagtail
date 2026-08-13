from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, Page


class ExperiencePage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    intro_heading = models.CharField(
        max_length=160, default="Professional Experience"
    )
    intro_text = models.TextField(
        default="A timeline of roles, responsibilities, and the systems I've built along the way."
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_heading"),
        FieldPanel("intro_text"),
        InlinePanel("entries", label="Experience entries"),
    ]


class ExperienceEntry(Orderable):
    page = ParentalKey(ExperiencePage, on_delete=models.CASCADE, related_name="entries")

    role_title = models.CharField(max_length=160)
    company_name = models.CharField(max_length=160)
    date_range = models.CharField(max_length=80, help_text="e.g. 2023 — Present")
    location = models.CharField(max_length=160, help_text="e.g. Kathmandu, Nepal (Remote)")
    is_current = models.BooleanField(
        default=False,
        help_text="Highlights this entry in emerald as the current role.",
    )
    bullet_points = models.TextField(
        help_text="One responsibility per line — rendered as a bullet list."
    )
    tech_tags = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated, e.g. Python, Django, Wagtail, FastAPI, PostgreSQL",
    )

    panels = [
        FieldPanel("role_title"),
        FieldPanel("company_name"),
        FieldPanel("date_range"),
        FieldPanel("location"),
        FieldPanel("is_current"),
        FieldPanel("bullet_points"),
        FieldPanel("tech_tags"),
    ]

    @property
    def bullet_list(self):
        return [line.strip() for line in self.bullet_points.splitlines() if line.strip()]

    @property
    def tech_tag_list(self):
        return [tag.strip() for tag in self.tech_tags.split(",") if tag.strip()]
