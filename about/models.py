from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class AboutPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    intro_heading = models.CharField(
        max_length=200,
        default="Engineering robust backend platforms with business clarity.",
    )
    intro_text = RichTextField(
        default="<p>An overview of my background, focus, and engineering mindset.</p>",
        features=["bold", "italic", "link"],
    )

    bio_heading = models.CharField(
        max_length=160, default="Professional Background & Value"
    )
    bio_paragraph_1 = RichTextField(features=["bold", "italic", "link"])
    bio_paragraph_2 = RichTextField(features=["bold", "italic", "link"])
    mindset_heading = models.CharField(max_length=160, default="Engineering Mindset")
    mindset_text = RichTextField(features=["bold", "italic", "link"])

    quick_facts_heading = models.CharField(max_length=80, default="Quick Facts")

    capabilities_eyebrow = models.CharField(
        max_length=80, default="Technical Skill Inventory"
    )
    capabilities_heading = models.CharField(
        max_length=160, default="Technologies & Capabilities"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_heading"),
        FieldPanel("intro_text"),
        FieldPanel("bio_heading"),
        FieldPanel("bio_paragraph_1"),
        FieldPanel("bio_paragraph_2"),
        InlinePanel("checklist_items", label="Core technical focus checklist"),
        FieldPanel("mindset_heading"),
        FieldPanel("mindset_text"),
        FieldPanel("quick_facts_heading"),
        InlinePanel("quick_facts", label="Quick facts"),
        FieldPanel("capabilities_eyebrow"),
        FieldPanel("capabilities_heading"),
        InlinePanel("skill_categories", label="Skill categories"),
    ]


class AboutPageChecklistItem(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="checklist_items")
    text = models.CharField(max_length=160)

    panels = [FieldPanel("text")]


class AboutPageQuickFact(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="quick_facts")
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=160)

    panels = [FieldPanel("label"), FieldPanel("value")]


class AboutPageSkillCategory(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="skill_categories")
    badge = models.CharField(max_length=4, help_text="e.g. BE, DB, CMS")
    title = models.CharField(max_length=120)
    items = RichTextField(features=["ul"])

    panels = [
        FieldPanel("badge"),
        FieldPanel("title"),
        FieldPanel("items"),
    ]
