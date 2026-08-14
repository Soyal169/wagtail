from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class AboutPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    intro_eyebrow = models.CharField(max_length=80, default="About Soyal")
    intro_heading = models.CharField(
        max_length=200,
        default="Developer background, engineering perspective & daily drivers.",
    )
    intro_text = RichTextField(
        default=(
            "<p>I'm a senior backend software developer based in Kathmandu, "
            "Nepal. I specialize in designing scalable database "
            "architectures, resilient REST APIs, and bespoke content "
            "management platforms using Python, Django, Wagtail CMS, and "
            "Laravel.</p>"
        ),
        features=["bold", "italic", "link"],
    )

    principles_heading = models.CharField(
        max_length=80, default="# Engineering Principles I Stand By"
    )

    workspace_heading = models.CharField(max_length=80, default="Workspace & Tooling")

    snapshot_cta_label = models.CharField(max_length=40, default="Let's Connect →")

    capabilities_eyebrow = models.CharField(
        max_length=80, default="Technical Inventory"
    )
    capabilities_heading = models.CharField(
        max_length=160, default="What I Bring to an Engineering Team"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("intro_eyebrow"),
                FieldPanel("intro_heading"),
                FieldPanel("intro_text"),
            ],
            heading="Page intro",
        ),
        InlinePanel("narrative_blocks", label="Story section"),
        MultiFieldPanel(
            [
                FieldPanel("principles_heading"),
                InlinePanel("checklist_items", label="Principle"),
            ],
            heading="Engineering principles callout",
        ),
        InlinePanel("quick_facts", label="Profile snapshot fact"),
        FieldPanel("snapshot_cta_label"),
        MultiFieldPanel(
            [
                FieldPanel("workspace_heading"),
                InlinePanel("workspace_rows", label="Workspace row"),
            ],
            heading="Workspace & tooling",
        ),
        MultiFieldPanel(
            [
                FieldPanel("capabilities_eyebrow"),
                FieldPanel("capabilities_heading"),
                InlinePanel("skill_categories", label="Skill category"),
            ],
            heading="Technical inventory",
        ),
    ]


class AboutPageNarrativeBlock(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="narrative_blocks")
    heading = models.CharField(max_length=160)
    body = RichTextField(features=["bold", "italic", "code", "link"])

    panels = [
        FieldPanel("heading"),
        FieldPanel("body"),
    ]


class AboutPageChecklistItem(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="checklist_items")
    text = models.CharField(max_length=200)

    panels = [FieldPanel("text")]


class AboutPageQuickFact(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="quick_facts")
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=160)
    accent = models.BooleanField(
        default=False, help_text="Renders this value in emerald (used for Availability)."
    )

    panels = [FieldPanel("label"), FieldPanel("value"), FieldPanel("accent")]


class AboutPageWorkspaceRow(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="workspace_rows")
    label = models.CharField(max_length=40)
    value = models.CharField(max_length=120)

    panels = [FieldPanel("label"), FieldPanel("value")]


class AboutPageSkillCategory(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="skill_categories")
    badge = models.CharField(max_length=4, help_text="e.g. 01")
    title = models.CharField(max_length=120)
    description = models.TextField(default="", blank=True)
    chips = models.CharField(
        max_length=200, default="", blank=True, help_text="Comma-separated badge chips"
    )

    panels = [
        FieldPanel("badge"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("chips"),
    ]

    @property
    def chip_list(self):
        return [c.strip() for c in self.chips.split(",") if c.strip()]
