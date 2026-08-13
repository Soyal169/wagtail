from django.core.exceptions import ValidationError
from django.db import models

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from modelcluster.fields import ParentalKey


def validate_terminal_json(value):
    required_top = {"identity", "services", "metrics"}
    if not isinstance(value, dict) or not required_top.issubset(value.keys()):
        raise ValidationError(
            "Terminal card JSON must be an object with 'identity', 'services', "
            "and 'metrics' keys."
        )
    identity = value.get("identity", {})
    if not isinstance(identity, dict) or not {"name", "role", "location", "status"}.issubset(identity.keys()):
        raise ValidationError(
            "'identity' must include name, role, location, and status."
        )
    if not isinstance(value.get("services"), list) or not value["services"]:
        raise ValidationError("'services' must be a non-empty list of strings.")
    metrics = value.get("metrics", {})
    if not isinstance(metrics, dict) or not {"uptime", "latency", "note"}.issubset(metrics.keys()):
        raise ValidationError("'metrics' must include uptime, latency, and note.")


class HomePage(Page):
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "about.AboutPage",
        "experience.ExperiencePage",
        "projects.ProjectsIndexPage",
        "blog.BlogIndexPage",
        "contact.ContactPage",
        "resume.ResumePage",
    ]

    hero_heading_main = models.CharField(
        max_length=200,
        default="Building software that ships reliable APIs.",
    )
    hero_heading_highlight = models.CharField(
        max_length=80,
        default="reliable APIs",
        help_text="Substring of the heading above to render with the gradient accent.",
    )
    hero_subhead = models.TextField(
        default=(
            "Senior backend developer specializing in Python, Django, Wagtail CMS, "
            "and Laravel — designing systems that scale from single-store POS "
            "platforms to enterprise content management."
        )
    )
    skill_pills = models.CharField(
        max_length=300,
        default="Python, Django, FastAPI, Laravel, Wagtail CMS, MySQL/PostgreSQL, REST APIs",
        help_text="Comma-separated list rendered as the 'Core Stack Expertise' pills.",
    )
    terminal_json = models.JSONField(
        default=dict,
        validators=[validate_terminal_json],
        help_text=(
            'Fake-terminal hero card content. Shape: {"identity": {"name", "role", '
            '"location", "status"}, "services": ["...", ...], "metrics": '
            '{"uptime", "latency", "note"}}'
        ),
    )

    featured_projects_eyebrow = models.CharField(max_length=80, default="Case Studies")
    featured_projects_heading = models.CharField(
        max_length=160, default="Featured Engineering Projects"
    )
    featured_projects_intro = models.TextField(
        default="A selection of production systems I've designed and built end to end."
    )

    philosophy_eyebrow = models.CharField(max_length=80, default="Engineering Philosophy")
    philosophy_heading = models.CharField(max_length=160, default="How I Build Software")
    philosophy_intro = models.TextField(
        default="Three principles that guide every system I design."
    )

    contact_cta_heading = models.CharField(
        max_length=160, default="Have a problem worth solving?"
    )
    contact_cta_text = RichTextField(
        default="<p>I'm always interested in hearing about new projects and opportunities.</p>",
        features=["bold", "italic", "link"],
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_heading_main"),
        FieldPanel("hero_heading_highlight"),
        FieldPanel("hero_subhead"),
        FieldPanel("skill_pills"),
        FieldPanel("terminal_json"),
        FieldPanel("featured_projects_eyebrow"),
        FieldPanel("featured_projects_heading"),
        FieldPanel("featured_projects_intro"),
        FieldPanel("philosophy_eyebrow"),
        FieldPanel("philosophy_heading"),
        FieldPanel("philosophy_intro"),
        InlinePanel("philosophy_steps", label="Philosophy steps"),
        FieldPanel("contact_cta_heading"),
        FieldPanel("contact_cta_text"),
    ]

    def get_context(self, request, *args, **kwargs):
        from projects.models import ProjectPage

        context = super().get_context(request, *args, **kwargs)
        context["featured_projects"] = (
            ProjectPage.objects.live()
            .filter(featured=True)
            .order_by("featured_order", "-first_published_at")[:4]
        )
        return context


class HomePagePhilosophyStep(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="philosophy_steps")
    number = models.CharField(max_length=4, help_text="e.g. 01")
    title = models.CharField(max_length=80)
    description = models.TextField()

    panels = [
        FieldPanel("number"),
        FieldPanel("title"),
        FieldPanel("description"),
    ]
