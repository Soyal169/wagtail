from django.core.exceptions import ValidationError
from django.db import models

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from modelcluster.fields import ParentalKey


def validate_terminal_json(value):
    """No longer used by any field — kept because home/migrations/0003
    imports and references this name when Django replays migration
    history, and deleting it would break that replay."""
    required_top = {"identity", "services", "metrics"}
    if not isinstance(value, dict) or not required_top.issubset(value.keys()):
        raise ValidationError(
            "Terminal card JSON must be an object with 'identity', 'services', "
            "and 'metrics' keys."
        )


ACCENT_CHOICES = [
    ("emerald", "Emerald"),
    ("amber", "Amber"),
    ("teal", "Teal"),
    ("purple", "Purple"),
]


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

    # --- 1. Hero -----------------------------------------------------------
    hero_heading_main = models.CharField(
        max_length=200,
        default="Hi, I'm Soyal.",
    )
    hero_heading_highlight = models.CharField(
        max_length=80,
        default="Soyal",
        help_text="Substring of the heading above to render with the accent color.",
    )
    hero_subhead = RichTextField(
        features=["bold", "italic", "link"],
        default=(
            "<p>I design and build production-grade web applications, "
            "high-concurrency APIs, resilient database architectures, and "
            "bespoke CMS platforms using <strong>Python (Django, Wagtail, "
            "FastAPI)</strong> and <strong>PHP (Laravel)</strong>.</p>"
        ),
    )
    portrait_role_chip = models.CharField(max_length=40, default="Backend Architect")
    portrait_caption_line = models.CharField(
        max_length=120,
        default="Specializing in Wagtail CMS, Django, FastAPI & Laravel",
    )
    terminal_filename = models.CharField(max_length=40, default="soyal_env.json")
    hero_cta_primary_label = models.CharField(max_length=40, default="View Selected Work")
    hero_cta_secondary_label = models.CharField(max_length=40, default="Let's Talk")
    hero_cta_ghost_label = models.CharField(max_length=40, default="CV / Resume")

    # --- 2. Developer snapshot ---------------------------------------------
    snapshot_eyebrow = models.CharField(max_length=80, default="Developer Snapshot")
    snapshot_note = models.CharField(max_length=80, default="Fast Facts & Environment")

    # --- 3. My story ---------------------------------------------------------
    story_eyebrow = models.CharField(max_length=80, default="About Soyal")
    story_heading = models.CharField(
        max_length=200,
        default="Engineering systems that are explicit, secure, and built to last.",
    )
    story_lede = models.TextField(
        default=(
            "I am a backend developer who cares deeply about schema integrity, "
            "clean domain boundaries, and creating interfaces that editorial "
            "teams actually enjoy using."
        )
    )
    story_link_text = models.CharField(max_length=80, default="Read my full journey and story →")
    story_body = RichTextField(
        features=["bold", "italic", "link"],
        default=(
            "<p>My journey into software engineering started in Kathmandu with "
            "a simple fascination: how can code reliably coordinate inventory, "
            "money, and content across distributed users without falling "
            "apart? That curiosity drove me straight to backend systems, "
            "database transactions, and content architectures.</p>"
            "<p>Over the years, I have architected and deployed production "
            "backends ranging from multi-outlet POS billing engines to "
            "headless e-commerce platforms and high-concurrency ticket "
            "locking systems. I specialize particularly in <strong>Wagtail "
            "CMS & Django</strong> because it provides the sweet spot of "
            "structured, flexible StreamField content authoring with the raw "
            "power and security of Python.</p>"
        ),
    )
    story_callout_heading = models.CharField(max_length=80, default="What Drives My Work Daily:")

    # --- 4. Core backend expertise -------------------------------------------
    expertise_eyebrow = models.CharField(max_length=80, default="Core Expertise")
    expertise_heading = models.CharField(
        max_length=160, default="Backend Engineering & System Architecture"
    )
    expertise_intro = models.TextField(
        default=(
            "Here is how I help engineering teams and businesses build fast, "
            "secure, and maintainable software."
        )
    )

    # --- 5. My toolbox --------------------------------------------------------
    toolbox_eyebrow = models.CharField(max_length=80, default="My Toolbox")
    toolbox_heading = models.CharField(max_length=160, default="Technologies & Daily Drivers")
    toolbox_note = models.CharField(
        max_length=120, default="Every tool here is used in production systems."
    )

    # --- 6. Featured projects -------------------------------------------------
    featured_projects_eyebrow = models.CharField(max_length=80, default="Production Work")
    featured_projects_heading = models.CharField(
        max_length=160, default="Featured Engineering Case Studies"
    )
    featured_projects_link_text = models.CharField(
        max_length=80, default="View all projects catalog →"
    )

    # --- 7. Engineering principles ---------------------------------------------
    philosophy_eyebrow = models.CharField(max_length=80, default="Engineering Principles")
    philosophy_heading = models.CharField(max_length=160, default="How I Think & Build Software")
    philosophy_intro = models.TextField(
        default=(
            "The guiding rules I follow when architecting systems for "
            "production stability and maintainability."
        )
    )

    # --- 8. Currently building & exploring ------------------------------------
    status_eyebrow = models.CharField(max_length=80, default="Live Status")
    status_heading = models.CharField(max_length=160, default="Currently Building & Exploring")
    status_updated_label = models.CharField(max_length=60, default="Updated August 2026")

    # --- 9. Beyond code ---------------------------------------------------------
    interests_eyebrow = models.CharField(max_length=80, default="Beyond The Terminal")
    interests_heading = models.CharField(max_length=160, default="Life Outside The Terminal")
    interests_lede = models.TextField(
        default="Great software is built by real people with broad perspectives and clear minds."
    )

    # --- 10. Let's connect CTA ---------------------------------------------------
    cta_eyebrow = models.CharField(max_length=80, default="Let's Build Together")
    contact_cta_heading = models.CharField(
        max_length=160, default="Have an interesting backend challenge or Wagtail project?"
    )
    contact_cta_text = RichTextField(
        default=(
            "<p>I am always interested in discussing senior backend "
            "engineering roles, Wagtail CMS architecture, and challenging "
            "database problems.</p>"
        ),
        features=["bold", "italic", "link"],
    )
    cta_button_label = models.CharField(max_length=40, default="Send Me a Message")
    cta_footnote = models.CharField(
        max_length=200,
        default="Based in Kathmandu, Nepal (UTC+5:45) • Usually responding within 24 hours.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_heading_main"),
                FieldPanel("hero_heading_highlight"),
                FieldPanel("hero_subhead"),
                FieldPanel("hero_cta_primary_label"),
                FieldPanel("hero_cta_secondary_label"),
                FieldPanel("hero_cta_ghost_label"),
                FieldPanel("portrait_role_chip"),
                FieldPanel("portrait_caption_line"),
                FieldPanel("terminal_filename"),
                InlinePanel("terminal_rows", label="Terminal row", max_num=4),
            ],
            heading="1 · Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("snapshot_eyebrow"),
                FieldPanel("snapshot_note"),
                InlinePanel("snapshot_facts", label="Snapshot fact", max_num=6),
            ],
            heading="2 · Developer snapshot",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("story_eyebrow"),
                FieldPanel("story_heading"),
                FieldPanel("story_lede"),
                FieldPanel("story_link_text"),
                FieldPanel("story_body"),
                FieldPanel("story_callout_heading"),
                InlinePanel("story_bullets", label="Callout bullet", max_num=3),
            ],
            heading="3 · My story",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("expertise_eyebrow"),
                FieldPanel("expertise_heading"),
                FieldPanel("expertise_intro"),
                InlinePanel("expertise_pillars", label="Expertise pillar", max_num=4),
            ],
            heading="4 · Core backend expertise",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("toolbox_eyebrow"),
                FieldPanel("toolbox_heading"),
                FieldPanel("toolbox_note"),
                InlinePanel(
                    "toolbox_rows",
                    label="Toolbox row",
                    help_text="Keep rows of the same category adjacent — they render grouped.",
                ),
            ],
            heading="5 · My toolbox",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("featured_projects_eyebrow"),
                FieldPanel("featured_projects_heading"),
                FieldPanel("featured_projects_link_text"),
            ],
            heading="6 · Featured projects",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("philosophy_eyebrow"),
                FieldPanel("philosophy_heading"),
                FieldPanel("philosophy_intro"),
                InlinePanel("philosophy_steps", label="Principle"),
            ],
            heading="7 · Engineering principles",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("status_eyebrow"),
                FieldPanel("status_heading"),
                FieldPanel("status_updated_label"),
                InlinePanel("status_cards", label="Status card", max_num=4),
            ],
            heading="8 · Currently building & exploring",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("interests_eyebrow"),
                FieldPanel("interests_heading"),
                FieldPanel("interests_lede"),
                InlinePanel("interests", label="Interest", max_num=4),
            ],
            heading="9 · Beyond code",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel("cta_eyebrow"),
                FieldPanel("contact_cta_heading"),
                FieldPanel("contact_cta_text"),
                FieldPanel("cta_button_label"),
                FieldPanel("cta_footnote"),
            ],
            heading="10 · Let's connect",
            classname="collapsible collapsed",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        from projects.models import ProjectPage

        context = super().get_context(request, *args, **kwargs)
        context["featured_projects"] = (
            ProjectPage.objects.live()
            .filter(featured=True)
            .order_by("featured_order", "-first_published_at")[:3]
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


class HomePageTerminalRow(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="terminal_rows")
    key = models.CharField(max_length=40)
    value = models.CharField(max_length=160)
    accent = models.CharField(max_length=10, choices=ACCENT_CHOICES, default="emerald")

    panels = [
        FieldPanel("key"),
        FieldPanel("value"),
        FieldPanel("accent"),
    ]


class HomePageSnapshotFact(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="snapshot_facts")
    label = models.CharField(max_length=40)
    value = models.CharField(max_length=60)
    sub_value = models.CharField(max_length=60)

    panels = [
        FieldPanel("label"),
        FieldPanel("value"),
        FieldPanel("sub_value"),
    ]


class HomePageStoryBullet(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="story_bullets")
    text = models.CharField(max_length=200)

    panels = [FieldPanel("text")]


class HomePageExpertisePillar(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="expertise_pillars")
    ordinal_label = models.CharField(max_length=40, help_text="e.g. 01 / APIS & CONCURRENCY")
    stack_badge = models.CharField(max_length=60, help_text="e.g. FastAPI • Django REST")
    heading = models.CharField(max_length=120)
    description = RichTextField(features=["bold", "italic", "code", "link"])
    chips = models.CharField(max_length=200, help_text="Comma-separated")

    panels = [
        FieldPanel("ordinal_label"),
        FieldPanel("stack_badge"),
        FieldPanel("heading"),
        FieldPanel("description"),
        FieldPanel("chips"),
    ]

    @property
    def chip_list(self):
        return [c.strip() for c in self.chips.split(",") if c.strip()]


class HomePageToolboxRow(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="toolbox_rows")
    category = models.CharField(
        max_length=60,
        help_text="Rows sharing a category render as one card; keep them adjacent.",
    )
    name = models.CharField(max_length=60)
    qualifier = models.CharField(max_length=40)
    highlight = models.BooleanField(default=False)

    panels = [
        FieldPanel("category"),
        FieldPanel("name"),
        FieldPanel("qualifier"),
        FieldPanel("highlight"),
    ]


class HomePageStatusCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="status_cards")
    emoji = models.CharField(max_length=8)
    category_label = models.CharField(max_length=40)
    accent = models.CharField(max_length=10, choices=ACCENT_CHOICES, default="emerald")
    title = models.CharField(max_length=120)
    description = models.TextField()

    panels = [
        FieldPanel("emoji"),
        FieldPanel("category_label"),
        FieldPanel("accent"),
        FieldPanel("title"),
        FieldPanel("description"),
    ]


class HomePageInterest(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="interests")
    emoji = models.CharField(max_length=8)
    label = models.CharField(max_length=60)
    heading = models.CharField(max_length=120)
    description = models.TextField()

    panels = [
        FieldPanel("emoji"),
        FieldPanel("label"),
        FieldPanel("heading"),
        FieldPanel("description"),
    ]
