from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from core.blocks import ArticleBodyBlock


@register_snippet
class ProjectCategory(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)

    panels = [FieldPanel("name"), FieldPanel("slug")]

    class Meta:
        verbose_name_plural = "Project categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProjectsIndexPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["projects.ProjectPage"]

    intro_eyebrow = models.CharField(max_length=80, default="Selected Work")
    intro_heading = models.CharField(max_length=160, default="Engineering Case Studies")
    intro_text = models.TextField(
        default="A closer look at the systems I've designed, built, and shipped."
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_eyebrow"),
        FieldPanel("intro_heading"),
        FieldPanel("intro_text"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["projects"] = (
            ProjectPage.objects.live().child_of(self).order_by("-first_published_at")
        )
        context["categories"] = ProjectCategory.objects.all()
        return context


class ProjectPage(Page):
    parent_page_types = ["projects.ProjectsIndexPage"]
    subpage_types = []

    categories = ParentalManyToManyField(ProjectCategory, related_name="projects")
    badge_label = models.CharField(
        max_length=80, help_text="Human-readable badge shown on the card, e.g. 'Real-Time System'"
    )
    tech_stack_summary = models.CharField(
        max_length=120, help_text="e.g. Laravel • Vue • MySQL"
    )
    tech_chips = models.CharField(
        max_length=200, help_text="Comma-separated short chips, e.g. Laravel 10, MySQL Schema, REST API"
    )
    summary = RichTextField(features=["bold", "italic", "link"])
    programming_language = models.CharField(
        max_length=160,
        help_text="Comma-separated, used for the SoftwareSourceCode JSON-LD, e.g. 'Python, Asyncio, WebSockets, Redis'",
    )
    featured = models.BooleanField(default=False)
    featured_order = models.PositiveIntegerField(
        null=True, blank=True, help_text="Lower numbers appear first among featured projects on the homepage."
    )

    body = StreamField(ArticleBodyBlock(), blank=True, use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("categories"),
        FieldPanel("badge_label"),
        FieldPanel("tech_stack_summary"),
        FieldPanel("tech_chips"),
        FieldPanel("summary"),
        FieldPanel("programming_language"),
        FieldPanel("featured"),
        FieldPanel("featured_order"),
        InlinePanel("stats", label="Stat grid rows"),
        FieldPanel("body"),
        InlinePanel("outcomes", label="Outcomes"),
    ]

    @property
    def tech_chip_list(self):
        return [chip.strip() for chip in self.tech_chips.split(",") if chip.strip()]

    @property
    def category_slugs(self):
        return " ".join(self.categories.values_list("slug", flat=True))


class ProjectStat(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name="stats")
    label = models.CharField(max_length=60)
    value = models.CharField(max_length=120)

    panels = [FieldPanel("label"), FieldPanel("value")]


class ProjectOutcome(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name="outcomes")
    text = models.TextField()

    panels = [FieldPanel("text")]
