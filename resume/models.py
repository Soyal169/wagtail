from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class ResumePage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    full_name = models.CharField(max_length=120, default="Soyal")
    tagline = models.CharField(
        max_length=160, default="Senior Backend Developer & Software Engineer"
    )
    contact_line = models.CharField(
        max_length=200,
        default="Kathmandu, Nepal · soyal@example.com",
        help_text="Rendered under the name/tagline, e.g. location and email.",
    )
    professional_summary = RichTextField(features=["bold", "italic"])
    education_line = models.CharField(
        max_length=200, help_text="Degree only, e.g. Bachelor of Science in Computer Science & Information Technology (BSc.CSIT)"
    )
    education_location = models.CharField(max_length=120, default="Kathmandu, Nepal")

    content_panels = Page.content_panels + [
        FieldPanel("full_name"),
        FieldPanel("tagline"),
        FieldPanel("contact_line"),
        FieldPanel("professional_summary"),
        InlinePanel("skill_categories", label="Technical skills"),
        InlinePanel("experience_entries", label="Work experience"),
        InlinePanel("project_highlights", label="Key featured projects"),
        FieldPanel("education_line"),
        FieldPanel("education_location"),
    ]


class ResumeSkillCategory(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name="skill_categories")
    label = models.CharField(max_length=60, help_text="e.g. Languages & Frameworks")
    values = models.CharField(max_length=300, help_text="Comma-separated skill list")

    panels = [FieldPanel("label"), FieldPanel("values")]

    @property
    def value_list(self):
        return [v.strip() for v in self.values.split(",") if v.strip()]


class ResumeExperienceEntry(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name="experience_entries")
    title = models.CharField(max_length=160, help_text="Role — Company")
    date_range = models.CharField(max_length=80)
    location = models.CharField(max_length=160)
    bullet_points = models.TextField(help_text="One condensed bullet per line.")

    panels = [
        FieldPanel("title"),
        FieldPanel("date_range"),
        FieldPanel("location"),
        FieldPanel("bullet_points"),
    ]

    @property
    def bullet_list(self):
        return [line.strip() for line in self.bullet_points.splitlines() if line.strip()]


class ResumeProjectHighlight(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name="project_highlights")
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200)

    panels = [FieldPanel("name"), FieldPanel("description")]
