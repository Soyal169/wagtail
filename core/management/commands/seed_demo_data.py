from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db import transaction

from about.models import AboutPage
from blog.models import BlogCategory, BlogIndexPage, BlogPostPage
from contact.models import ContactPage
from core.models import SiteBrandSettings
from experience.models import ExperiencePage
from home.models import HomePage
from projects.models import ProjectCategory, ProjectsIndexPage, ProjectPage
from resume.models import ResumePage
from wagtail.images.models import Image
from wagtail.models import Site


def sync_children(page, related_name, rows):
    """Idempotent child-row sync: these are presentation-only rows with no
    independent identity worth preserving across re-runs, so delete and
    recreate from the seed data every time.

    Page is a ClusterableModel, so its child relation managers buffer
    creates/deletes in memory — page.save() is required to flush them to
    the database.
    """
    manager = getattr(page, related_name)
    manager.all().delete()
    for row in rows:
        manager.create(**row)
    page.save()


def _seed_portrait():
    """Idempotent by title: loads the prototype's portrait photo into a
    Wagtail Image once, no-ops if the source file is missing (e.g. a
    checkout without static_prototype/)."""
    image = Image.objects.filter(title="Soyal portrait").first()
    if image is not None:
        return image
    path = Path(settings.BASE_DIR) / "static_prototype" / "assets" / "images" / "profile.jpg"
    if not path.exists():
        return None
    image = Image(
        title="Soyal portrait",
        description=(
            "Soyal — Senior Backend Developer & Wagtail Specialist in "
            "Kathmandu, Nepal"
        ),
    )
    with path.open("rb") as fh:
        image.file = ImageFile(fh, name="soyal-portrait.jpg")
        image.save()
    return image


def upsert_child_page(parent, model, slug, field_values):
    page = model.objects.child_of(parent).filter(slug=slug).first()
    if page is None:
        page = model(slug=slug, **field_values)
        parent.add_child(instance=page)
    else:
        for key, value in field_values.items():
            setattr(page, key, value)
        page.save()
    page.save_revision().publish()
    return page


class Command(BaseCommand):
    help = "Seeds the database with all content from the original static prototype."

    def handle(self, *args, **options):
        with transaction.atomic():
            site = Site.objects.get(is_default_site=True)
            self._seed_site_settings(site)
            home = self._seed_home_page(site)
            self._seed_about_page(home)
            self._seed_experience_page(home)
            projects_index = self._seed_projects_index(home)
            self._seed_project_pages(projects_index)
            blog_index = self._seed_blog_index(home)
            self._seed_blog_pages(blog_index)
            self._seed_contact_page(home)
            self._seed_resume_page(home)
        self.stdout.write(self.style.SUCCESS("Seed complete."))

    # ------------------------------------------------------------------
    # Site settings
    # ------------------------------------------------------------------
    def _seed_site_settings(self, site):
        brand = SiteBrandSettings.for_site(site)
        brand.site_name = "Soyal.dev"
        brand.tagline = "Senior Backend Developer & Wagtail Specialist"
        brand.footer_blurb = (
            "Senior Backend Developer & Wagtail Specialist based in Kathmandu, Nepal. "
            "Building production backend systems with Django, Wagtail, FastAPI, and Laravel."
        )
        brand.location = "Kathmandu, Nepal"
        brand.timezone_label = "UTC+5:45"
        brand.availability_status = "Open to Senior Backend Roles & Consultancy"
        brand.contact_email = "soyal@example.com"
        brand.github_url = "https://github.com/soyal"
        brand.linkedin_url = "https://linkedin.com/in/soyal"
        brand.person_name = "Soyal"
        brand.person_job_title = "Senior Backend Developer & Wagtail Specialist"
        brand.knows_about = (
            "Python, Django, Wagtail CMS, FastAPI, PHP, Laravel, PostgreSQL, MySQL, "
            "Redis, Docker, REST API Architecture"
        )
        brand.org_name = "Independent Engineering Consultant"
        brand.portrait = _seed_portrait()
        brand.portrait_caption = "soyal.portrait"
        brand.coordinates = "27.7172° N, 85.3240° E"
        brand.save()

    # ------------------------------------------------------------------
    # Home
    # ------------------------------------------------------------------
    def _seed_home_page(self, site):
        home = site.root_page.specific
        if not isinstance(home, HomePage):
            raise RuntimeError("Expected the site root page to be a HomePage.")

        home.title = "Home"
        home.seo_title = "Soyal | Senior Backend Developer & Wagtail Specialist (Kathmandu, Nepal)"
        home.search_description = (
            "Personal portfolio of Soyal — Senior Backend Developer & Wagtail Specialist "
            "based in Kathmandu, Nepal. Crafting resilient REST APIs, database "
            "architectures, and CMS platforms with Python, Django, Wagtail, FastAPI, "
            "and Laravel."
        )

        # 1. Hero
        home.hero_heading_main = "Hi, I'm Soyal."
        home.hero_heading_highlight = "Soyal"
        home.hero_subhead = (
            "<p>I design and build production-grade web applications, "
            "high-concurrency APIs, resilient database architectures, and "
            "bespoke CMS platforms using <strong>Python (Django, Wagtail, "
            "FastAPI)</strong> and <strong>PHP (Laravel)</strong>.</p>"
        )
        home.portrait_role_chip = "Backend Architect"
        home.portrait_caption_line = "Specializing in Wagtail CMS, Django, FastAPI & Laravel"
        home.terminal_filename = "soyal_env.json"
        home.hero_cta_primary_label = "View Selected Work"
        home.hero_cta_secondary_label = "Let's Talk"
        home.hero_cta_ghost_label = "CV / Resume"

        # 2. Developer snapshot
        home.snapshot_eyebrow = "Developer Snapshot"
        home.snapshot_note = "Fast Facts & Environment"

        # 3. My story
        home.story_eyebrow = "About Soyal"
        home.story_heading = "Engineering systems that are explicit, secure, and built to last."
        home.story_lede = (
            "I am a backend developer who cares deeply about schema integrity, "
            "clean domain boundaries, and creating interfaces that editorial "
            "teams actually enjoy using."
        )
        home.story_link_text = "Read my full journey and story →"
        home.story_body = (
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
        )
        home.story_callout_heading = "What Drives My Work Daily:"

        # 4. Core backend expertise
        home.expertise_eyebrow = "Core Expertise"
        home.expertise_heading = "Backend Engineering & System Architecture"
        home.expertise_intro = (
            "Here is how I help engineering teams and businesses build fast, "
            "secure, and maintainable software."
        )

        # 5. My toolbox
        home.toolbox_eyebrow = "My Toolbox"
        home.toolbox_heading = "Technologies & Daily Drivers"
        home.toolbox_note = "Every tool here is used in production systems."

        # 6. Featured projects
        home.featured_projects_eyebrow = "Production Work"
        home.featured_projects_heading = "Featured Engineering Case Studies"
        home.featured_projects_link_text = "View all projects catalog →"

        # 7. Engineering principles
        home.philosophy_eyebrow = "Engineering Principles"
        home.philosophy_heading = "How I Think & Build Software"
        home.philosophy_intro = (
            "The guiding rules I follow when architecting systems for "
            "production stability and maintainability."
        )

        # 8. Currently building & exploring
        home.status_eyebrow = "Live Status"
        home.status_heading = "Currently Building & Exploring"
        home.status_updated_label = "Updated August 2026"

        # 9. Beyond code
        home.interests_eyebrow = "Beyond The Terminal"
        home.interests_heading = "Life Outside The Terminal"
        home.interests_lede = (
            "Great software is built by real people with broad perspectives "
            "and clear minds."
        )

        # 10. Let's connect
        home.cta_eyebrow = "Let's Build Together"
        home.contact_cta_heading = "Have an interesting backend challenge or Wagtail project?"
        home.contact_cta_text = (
            "<p>I am always interested in discussing senior backend "
            "engineering roles, Wagtail CMS architecture, and challenging "
            "database problems.</p>"
        )
        home.cta_button_label = "Send Me a Message"
        home.cta_footnote = (
            "Based in Kathmandu, Nepal (UTC+5:45) • Usually responding within 24 hours."
        )

        home.save()
        home.save_revision().publish()

        sync_children(home, "terminal_rows", [
            {"key": "role", "value": "Senior Backend Engineer", "accent": "emerald"},
            {"key": "core_cms", "value": "Wagtail (Django)", "accent": "amber"},
            {"key": "api_engines", "value": '["FastAPI", "Django REST", "Laravel"]', "accent": "teal"},
            {"key": "db_discipline", "value": "ACID • PostgreSQL • Redis Locks", "accent": "purple"},
        ])

        sync_children(home, "snapshot_facts", [
            {"label": "Based in", "value": "Kathmandu, Nepal", "sub_value": "UTC+5:45 Timezone"},
            {"label": "Core Discipline", "value": "Backend & CMS", "sub_value": "High-concurrency APIs"},
            {"label": "Specialization", "value": "Wagtail CMS", "sub_value": "StreamFields & Models"},
            {"label": "Primary Stack", "value": "Python / PHP", "sub_value": "Django, FastAPI, Laravel"},
            {"label": "Storage & Cache", "value": "PostgreSQL / Redis", "sub_value": "ACID locks & Caching"},
            {"label": "Daily Drivers", "value": "Neovim / Docker", "sub_value": "Postman & DBeaver"},
        ])

        sync_children(home, "story_bullets", [
            {"text": "Writing clean, self-documenting code over convoluted abstractions."},
            {"text": "Designing database tables with explicit foreign keys, indexes, and concurrency locks."},
            {"text": "Giving editorial and business teams flexible CMS building blocks without breaking layouts."},
        ])

        sync_children(home, "expertise_pillars", [
            {
                "ordinal_label": "01 / APIS & CONCURRENCY",
                "stack_badge": "FastAPI • Django REST",
                "heading": "REST APIs & Async Microservices",
                "description": (
                    "<p>Designing predictable REST endpoints, rate limiting, token "
                    "authentication (JWT / OAuth2), and asynchronous worker pipelines "
                    "with sub-second response times.</p>"
                ),
                "chips": "Asyncio, Redis Locks, Pydantic, WebSockets",
            },
            {
                "ordinal_label": "02 / CMS ARCHITECTURE",
                "stack_badge": "Wagtail CMS • Django",
                "heading": "Wagtail CMS & Content Hubs",
                "description": (
                    "<p>Building modular Wagtail Page Models and bespoke StreamField "
                    "block ecosystems. Empowering non-technical content teams while "
                    "keeping HTML semantic and cached.</p>"
                ),
                "chips": "StreamFields, PageChooser, Snippets, Redis Cache",
            },
            {
                "ordinal_label": "03 / DATABASE DESIGN",
                "stack_badge": "PostgreSQL • MySQL",
                "heading": "Schema Design & ACID Transactions",
                "description": (
                    "<p>Normalizing relational tables, crafting multi-tenant tenant "
                    "isolation keys, pessimistic locking (<code>lockForUpdate</code>), "
                    "and profiling ORM query performance.</p>"
                ),
                "chips": "Query Profiling, Index Strategy, Transactions, N+1 Elimination",
            },
            {
                "ordinal_label": "04 / BUSINESS SYSTEMS",
                "stack_badge": "Laravel • Vue",
                "heading": "POS & Commercial Integrations",
                "description": (
                    "<p>Engineering multi-outlet billing systems, inventory deduction "
                    "engines, kitchen display ticket dispatchers, and reliable webhook "
                    "ingestion pipelines.</p>"
                ),
                "chips": "Multi-Store POS, Payment Webhooks, Audit Logs, REST Sync",
            },
        ])

        sync_children(home, "toolbox_rows", [
            {"category": "Backend & CMS", "name": "Python 3.11+", "qualifier": "Core", "highlight": False},
            {"category": "Backend & CMS", "name": "Django & DRF", "qualifier": "Primary", "highlight": False},
            {"category": "Backend & CMS", "name": "Wagtail CMS", "qualifier": "Specialist", "highlight": True},
            {"category": "Backend & CMS", "name": "FastAPI", "qualifier": "Async", "highlight": False},
            {"category": "Backend & CMS", "name": "PHP & Laravel", "qualifier": "Web/POS", "highlight": False},
            {"category": "Databases & Caching", "name": "PostgreSQL", "qualifier": "Primary", "highlight": True},
            {"category": "Databases & Caching", "name": "Redis", "qualifier": "Locks & Cache", "highlight": False},
            {"category": "Databases & Caching", "name": "MySQL / MariaDB", "qualifier": "Commercial", "highlight": False},
            {"category": "Databases & Caching", "name": "SQLite", "qualifier": "Testing", "highlight": False},
            {"category": "DevOps & Tooling", "name": "Docker & Compose", "qualifier": "Containers", "highlight": False},
            {"category": "DevOps & Tooling", "name": "Git & GitHub", "qualifier": "VCS", "highlight": False},
            {"category": "DevOps & Tooling", "name": "Postman", "qualifier": "API Testing", "highlight": False},
            {"category": "DevOps & Tooling", "name": "DBeaver / DataGrip", "qualifier": "DB GUI", "highlight": False},
            {"category": "DevOps & Tooling", "name": "Linux / Bash / Zsh", "qualifier": "Shell", "highlight": False},
            {"category": "Frontend & Interfaces", "name": "JavaScript (ES6+)", "qualifier": "Vanilla", "highlight": False},
            {"category": "Frontend & Interfaces", "name": "Vue.js", "qualifier": "POS UI", "highlight": False},
            {"category": "Frontend & Interfaces", "name": "Tailwind CSS", "qualifier": "Styling", "highlight": False},
            {"category": "Frontend & Interfaces", "name": "HTML5 / Semantic", "qualifier": "Clean", "highlight": False},
        ])

        sync_children(home, "philosophy_steps", [
            {
                "number": "01",
                "title": "Understand Before Coding",
                "description": (
                    "Identify edge cases, state transitions, and concurrency hazards "
                    "before writing a single line of application code."
                ),
            },
            {
                "number": "02",
                "title": "Schema-First Modeling",
                "description": (
                    "If the database schema is clean and explicit, business logic "
                    "remains simple. If the schema is flawed, everything else becomes "
                    "technical debt."
                ),
            },
            {
                "number": "03",
                "title": "Explicit Over Clever",
                "description": (
                    "Code is read ten times more often than it is written. I prefer "
                    "boring, explicit patterns over cryptic \"magical\" metaprogramming."
                ),
            },
            {
                "number": "04",
                "title": "Defense in Depth",
                "description": (
                    "Validate input on the edge (Pydantic / FormRequest), verify "
                    "permissions in middleware, and lock resources at the database "
                    "row level."
                ),
            },
            {
                "number": "05",
                "title": "Measure Before Optimizing",
                "description": (
                    "Never guess what is slow. Profile SQL execution plans "
                    "(EXPLAIN ANALYZE) and benchmark endpoints before refactoring."
                ),
            },
            {
                "number": "06",
                "title": "Empathy for Editors",
                "description": (
                    "A CMS is only as good as the editor experience. Wagtail "
                    "StreamFields should guide content managers without putting "
                    "cognitive load on them."
                ),
            },
        ])

        sync_children(home, "status_cards", [
            {
                "emoji": "🔨",
                "category_label": "Currently Building",
                "accent": "emerald",
                "title": "High-Throughput Redis Event Streamer",
                "description": (
                    "Evaluating consumer group offsets and async Python workers for "
                    "distributed task queues."
                ),
            },
            {
                "emoji": "🔍",
                "category_label": "Deep Diving",
                "accent": "amber",
                "title": "Wagtail 6 & Async Django ORM",
                "description": (
                    "Benchmarking async query evaluation inside custom Wagtail Page "
                    "get_context methods."
                ),
            },
            {
                "emoji": "📖",
                "category_label": "Reading",
                "accent": "teal",
                "title": "Designing Data-Intensive Apps",
                "description": (
                    "Revisiting partition strategies, replication lag handling, and "
                    "consensus models by Martin Kleppmann."
                ),
            },
            {
                "emoji": "💼",
                "category_label": "Open To",
                "accent": "purple",
                "title": "Senior Roles & Consultancy",
                "description": (
                    "Available for full-time senior backend roles and Wagtail CMS "
                    "architecture consultation."
                ),
            },
        ])

        sync_children(home, "interests", [
            {
                "emoji": "🏔️",
                "label": "Himalayan Trails",
                "heading": "Hiking & Trail Exploration",
                "description": (
                    "Hiking the ridge trails of the Kathmandu valley and surrounding "
                    "Himalayan foothills to reset and rethink complex systems."
                ),
            },
            {
                "emoji": "👥",
                "label": "Mentoring & Community",
                "heading": "Local Tech Community",
                "description": (
                    "Helping junior developers understand relational schema design, "
                    "API security, and Python best practices."
                ),
            },
            {
                "emoji": "☕",
                "label": "Coffee & Deep Work",
                "heading": "Manual Pour-Overs",
                "description": (
                    "Daily coffee brewing rituals that set the rhythm for focused, "
                    "uninterrupted deep work sessions."
                ),
            },
            {
                "emoji": "⌨️",
                "label": "Craft & Keyboards",
                "heading": "Tactile Hardware Setup",
                "description": (
                    "Enjoying clean, minimalist hardware setups, customized keymaps, "
                    "and high-contrast monospace code themes."
                ),
            },
        ])
        return home

    # ------------------------------------------------------------------
    # About
    # ------------------------------------------------------------------
    def _seed_about_page(self, home):
        about = upsert_child_page(home, AboutPage, "about", {
            "title": "About",
            "seo_title": "About Me | Soyal — Senior Backend Developer & Wagtail Specialist",
            "search_description": (
                "Learn about Soyal, a Senior Backend Developer in Kathmandu, Nepal "
                "specializing in Python, Django, Wagtail CMS, FastAPI, and Laravel "
                "architecture."
            ),
            "intro_eyebrow": "About Soyal",
            "intro_heading": "Developer background, engineering perspective & daily drivers.",
            "intro_text": (
                "<p>I'm a senior backend software developer based in Kathmandu, "
                "Nepal. I specialize in designing scalable database "
                "architectures, resilient REST APIs, and bespoke content "
                "management platforms using Python, Django, Wagtail CMS, and "
                "Laravel.</p>"
            ),
            "principles_heading": "# Engineering Principles I Stand By",
            "workspace_heading": "Workspace & Tooling",
            "snapshot_cta_label": "Let's Connect →",
            "capabilities_eyebrow": "Technical Inventory",
            "capabilities_heading": "What I Bring to an Engineering Team",
        })

        sync_children(about, "narrative_blocks", [
            {
                "heading": "My Background & How I Got Into Engineering",
                "body": (
                    "<p>My entry into software engineering was driven by solving "
                    "concrete operational problems in Kathmandu. I wanted to "
                    "understand how commercial platforms handle thousands of "
                    "orders, manage inventory across disparate retail locations, "
                    "and prevent data corruption under load.</p>"
                    "<p>Over the years, I moved from building foundational "
                    "database queries to architecting distributed applications "
                    "— including multi-counter POS systems, high-concurrency "
                    "ticket locking engines in FastAPI, and scalable Wagtail CMS "
                    "publishing systems.</p>"
                ),
            },
            {
                "heading": "Why I Specialize in Wagtail CMS & Django",
                "body": (
                    "<p>Content management platforms frequently fail on one of "
                    "two axes: they either provide a rigid developer experience "
                    "that resists customization, or they hand editors an unruly "
                    "visual builder that destroys layout consistency.</p>"
                    "<p>Wagtail CMS solves this with Pythonic elegance. By "
                    "combining Django's hardened ORM with Wagtail's "
                    "<code>StreamField</code> components and custom page models, "
                    "I deliver rich, structured editorial interfaces while "
                    "ensuring fast load times and clean database schemas.</p>"
                ),
            },
            {
                "heading": "What Motivates Me",
                "body": (
                    "<p>I get genuine satisfaction from turning ambiguous, "
                    "tangled business requirements into clean, self-documenting "
                    "code with predictable database indexes and sub-100ms "
                    "response times. I believe great backend engineering makes "
                    "the entire organization faster, safer, and more "
                    "resilient.</p>"
                ),
            },
        ])
        sync_children(about, "checklist_items", [
            {"text": "Relational schema integrity over fragile application-layer workarounds."},
            {"text": "Explicit, readable functions over dense, \"magical\" abstractions."},
            {"text": "Strict request validation and sanitized boundaries on every endpoint."},
            {"text": "Profile query plans (EXPLAIN ANALYZE) before throwing cache layers at unoptimized SQL."},
        ])
        sync_children(about, "quick_facts", [
            {"label": "Location", "value": "Kathmandu, Nepal (UTC+5:45)", "accent": False},
            {"label": "Specialization", "value": "Backend & Wagtail CMS", "accent": False},
            {"label": "Core Languages", "value": "Python, PHP, SQL", "accent": False},
            {"label": "Availability", "value": "Senior Roles & Consultancy", "accent": True},
        ])
        sync_children(about, "workspace_rows", [
            {"label": "Editor", "value": "VS Code / Neovim"},
            {"label": "Terminal", "value": "Zsh + Oh My Zsh"},
            {"label": "Database", "value": "DBeaver / PostgreSQL CLI"},
            {"label": "Runtime", "value": "Docker & Docker Compose"},
            {"label": "API Tool", "value": "Postman / HTTPie"},
        ])
        sync_children(about, "skill_categories", [
            {
                "badge": "01",
                "title": "Backend Systems & APIs",
                "description": (
                    "Designing scalable application backends, clean API "
                    "contracts, role-based authorization (RBAC), and "
                    "background job workers."
                ),
                "chips": "Python, Django, FastAPI, PHP, Laravel, REST APIs",
            },
            {
                "badge": "02",
                "title": "Wagtail CMS & Publishing",
                "description": (
                    "Crafting modular StreamFields, custom page hierarchy "
                    "trees, custom Django admin panels, and headless content "
                    "API delivery."
                ),
                "chips": "Wagtail CMS, StreamField, Page Models, Snippets, Headless APIs",
            },
            {
                "badge": "03",
                "title": "Databases & Infrastructure",
                "description": (
                    "Relational data modeling, compound index optimization, "
                    "transaction isolation levels, Redis mutex locks, and "
                    "Docker pipelines."
                ),
                "chips": "PostgreSQL, MySQL, Redis, Docker, Git / CI/CD",
            },
        ])

    # ------------------------------------------------------------------
    # Experience
    # ------------------------------------------------------------------
    def _seed_experience_page(self, home):
        experience = upsert_child_page(home, ExperiencePage, "experience", {
            "title": "Experience",
            "seo_title": "Engineering Experience & Roles | Soyal Backend Developer Nepal",
            "search_description": (
                "Career timeline and engineering experience of Soyal — Senior Backend Developer "
                "specializing in Python, Django, FastAPI, Laravel, REST APIs, and database engineering."
            ),
            "intro_heading": "Career Experience & Technical Impact",
            "intro_text": (
                "A chronological timeline of engineering roles, system architecture "
                "contributions, and backend business solutions delivered across web software systems."
            ),
        })

        sync_children(experience, "entries", [
            {
                "role_title": "Senior Backend Developer",
                "company_name": "Enterprise Software Solutions",
                "date_range": "2023 — Present",
                "location": "Kathmandu, Nepal (Remote)",
                "is_current": True,
                "bullet_points": (
                    "Architected REST APIs in Python (FastAPI/Django) serving multi-tenant POS "
                    "platforms and real-time inventory synchronization.\n"
                    "Designed Wagtail CMS custom page models and StreamFields for content "
                    "editors with zero code deployments.\n"
                    "Optimized PostgreSQL database query indexing, reducing long-running "
                    "analytics query times by eliminating N+1 executions.\n"
                    "Implemented OAuth2 and JWT authentication flows with granular "
                    "role-based permissions (RBAC)."
                ),
                "tech_tags": "Python, Django, Wagtail, FastAPI, PostgreSQL",
            },
            {
                "role_title": "Full-Stack Software Engineer",
                "company_name": "Web Application Studio",
                "date_range": "2021 — 2023",
                "location": "Kathmandu, Nepal",
                "is_current": False,
                "bullet_points": (
                    "Built NexusPOS using Laravel and Vue.js, supporting multi-outlet store "
                    "billing, kitchen display order routing, and inventory tracking.\n"
                    "Integrated payment gateway API webhooks with transaction verification "
                    "and fallback logs.\n"
                    "Maintained and extended WordPress and WooCommerce backend custom "
                    "plugins for e-commerce clients."
                ),
                "tech_tags": "PHP, Laravel, MySQL, Vue.js, REST APIs",
            },
            {
                "role_title": "Junior Developer & Systems Trainee",
                "company_name": "Technology Labs",
                "date_range": "2020 — 2021",
                "location": "Kathmandu, Nepal",
                "is_current": False,
                "bullet_points": (
                    "Constructed database schemas, SQL migrations, and basic CRUD "
                    "services in Python and PHP.\n"
                    "Documented REST API specifications using Swagger/OpenAPI and "
                    "assisted in client frontend integration testing.\n"
                    "Maintained git version control branches and resolved merge "
                    "conflicts across sprint cycles."
                ),
                "tech_tags": "Python, PHP, SQL, Git, Linux",
            },
        ])

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------
    def _seed_projects_index(self, home):
        return upsert_child_page(home, ProjectsIndexPage, "projects", {
            "title": "Projects",
            "seo_title": "Software & Backend Engineering Projects | Soyal Developer",
            "search_description": (
                "Explore production backend projects, POS software, booking engines, Wagtail "
                "CMS integrations, and APIs built by Soyal in Kathmandu, Nepal."
            ),
            "intro_eyebrow": "Case Studies",
            "intro_heading": "Production Engineering Projects & Case Studies",
            "intro_text": (
                "Detailed technical breakdowns of business applications, point of sale "
                "software, cinema booking engines, and Wagtail CMS architecture."
            ),
        })

    def _seed_project_pages(self, projects_index):
        backend = ProjectCategory.objects.get_or_create(slug="backend", defaults={"name": "Backend & APIs"})[0]
        fullstack = ProjectCategory.objects.get_or_create(slug="fullstack", defaults={"name": "Full-Stack / POS"})[0]
        cms = ProjectCategory.objects.get_or_create(slug="cms", defaults={"name": "CMS & E-commerce"})[0]

        projects = [
            {
                "slug": "nexuspos",
                "title": "NexusPOS — Multi-Store Point of Sale Platform",
                "seo_title": "NexusPOS Case Study — Multi-Store POS Platform | Soyal",
                "search_description": (
                    "Technical Case Study: Architecture, database schema design, and Laravel "
                    "REST API implementation for NexusPOS multi-outlet point of sale platform."
                ),
                "categories": [fullstack, backend],
                "badge_label": "Full-Stack / POS",
                "tech_stack_summary": "Laravel • Vue.js • MySQL",
                "tech_chips": "Laravel 10, MySQL Schema, REST API",
                "summary": (
                    "<p>Engineering a scalable multi-outlet inventory, kitchen order routing, "
                    "and billing system with real-time stock synchronization and transaction "
                    "isolation.</p>"
                ),
                "programming_language": "PHP, Laravel, Vue.js, MySQL",
                "featured": True,
                "featured_order": 1,
                "role_label": "Lead Backend Engineer",
                "core_problem": "Multi-branch real-time stock sync & race conditions",
                "solution": "Atomic row locks + offline receipt sync pipeline",
                "architecture_highlight": (
                    "Guaranteed zero stock overselling across 5+ concurrent billing "
                    "counters per store."
                ),
                "stats": [
                    {"label": "My Role", "value": "Lead Backend Engineer"},
                    {"label": "Primary Tech", "value": "Laravel, Vue, MySQL"},
                    {"label": "Scope", "value": "Multi-outlet POS API"},
                    {"label": "Target Sector", "value": "Retail & Hospitality"},
                ],
                "body": [
                    ("heading", "1. Problem Statement & Context"),
                    ("paragraph", (
                        "<p>Retailers and restaurant outlets managing multiple physical stores "
                        "frequently face inventory discrepancies when sales happen concurrently "
                        "at different billing counters. Without atomic stock deduction, stock "
                        "counts drift out of sync, causing stockouts and incorrect financial "
                        "reports.</p>"
                    )),
                    ("heading", "2. System Architecture"),
                    ("diagram", {
                        "nodes": [
                            {"label": "POS Terminal Client", "sublabel": "Vue.js / Offline Cache"},
                            {"label": "Laravel Core Engine", "sublabel": "DB Transactions & Locks"},
                        ]
                    }),
                    ("paragraph", (
                        "<p>Key feature: All inventory movements are wrapped inside database "
                        "transactions with pessimistic row locking (<code>SELECT FOR UPDATE</code>) "
                        "to guarantee stock isolation.</p>"
                    )),
                    ("heading", "3. Implementation & Database Isolation"),
                    ("paragraph", (
                        "<p>The backend exposes structured REST endpoints for cashier "
                        "authentication, catalog fetching, invoice generation, and kitchen "
                        "ticket dispatching.</p>"
                    )),
                    ("code", {
                        "language": "php",
                        "filename": "",
                        "code": (
                            "// Atomic stock deduction logic pattern\n"
                            "DB::transaction(function () use ($outletId, $items) {\n"
                            "    foreach ($items as $item) {\n"
                            "        $stock = OutletStock::where('outlet_id', $outletId)\n"
                            "            ->where('product_id', $item['product_id'])\n"
                            "            ->lockForUpdate()\n"
                            "            ->firstOrFail();\n\n"
                            "        $stock->decrement('quantity', $item['qty']);\n"
                            "    }\n"
                            "});"
                        ),
                    }),
                ],
                "outcomes": [
                    "Achieved zero stock discrepancy errors under multi-counter concurrent sales tests.",
                    "Reduced kitchen display order lag to under 200ms using lightweight polling and efficient payload design.",
                    "Reinforced the importance of explicit database row locking when building commercial transaction software.",
                ],
            },
            {
                "slug": "cinema-platform",
                "title": "Cinema Ticket Reservation Engine",
                "seo_title": "Cinema Booking Engine Case Study — FastAPI & Redis | Soyal",
                "search_description": (
                    "Technical Case Study: High-concurrency seat reservation system built with "
                    "Python FastAPI, Redis distributed locking, and PostgreSQL."
                ),
                "categories": [backend],
                "badge_label": "Backend API",
                "tech_stack_summary": "FastAPI • Redis • PostgreSQL",
                "tech_chips": "FastAPI, Redis Lock, PostgreSQL",
                "summary": (
                    "<p>Designing a high-concurrency seat reservation API using FastAPI async "
                    "workers, temporary Redis locks, and idempotent payment webhooks.</p>"
                ),
                "programming_language": "Python, FastAPI, Redis",
                "featured": True,
                "featured_order": 2,
                "role_label": "Backend Architect",
                "core_problem": "Hundreds of simultaneous checkout requests for same seat",
                "solution": "Sub-20ms Redis distributed mutex locks with TTLs",
                "architecture_highlight": (
                    "Dropped SQL contention by 65% by shifting temporary holds into "
                    "Redis memory."
                ),
                "stats": [
                    {"label": "My Role", "value": "Backend Architect"},
                    {"label": "Tech Stack", "value": "FastAPI, Redis, Postgres"},
                    {"label": "Primary Problem", "value": "Race Condition Locking"},
                    {"label": "Lock Duration", "value": "10 Minutes (TTL)"},
                ],
                "body": [
                    ("heading", "1. Problem Statement"),
                    ("paragraph", (
                        "<p>During blockbuster movie ticket releases, thousands of users hit "
                        "the seat selection screen simultaneously. Standard SQL row updates "
                        "cause database lock contention or double bookings when two customers "
                        "select Seat E-12 at the exact same millisecond.</p>"
                    )),
                    ("heading", "2. Redis Distributed Lock Strategy"),
                    ("paragraph", (
                        "<p>We implemented a 10-minute temporary seat reservation mechanism in "
                        "Redis before committing the ticket record to PostgreSQL.</p>"
                    )),
                    ("code", {
                        "language": "python",
                        "filename": "",
                        "code": (
                            "# FastAPI Seat Lock Endpoint\n"
                            "@router.post(\"/showtimes/{id}/reserve\")\n"
                            "async def reserve_seats(showtime_id: int, seats: List[str], user_id: int):\n"
                            "    lock_key = f\"lock:showtime:{showtime_id}:seat:{seat}\"\n"
                            "    # Acquire Redis Key with 600 second expiration\n"
                            "    acquired = await redis.set(lock_key, user_id, nx=True, ex=600)\n"
                            "    if not acquired:\n"
                            "        raise HTTPException(status_code=409, detail=\"Seat temporarily held by another user\")\n"
                            "    return {\"status\": \"reserved\", \"ttl\": 600}"
                        ),
                    }),
                    ("heading", "3. Outcomes"),
                    ("paragraph", (
                        "<p>Zero double bookings registered across 50,000+ test ticket "
                        "transactions, and PostgreSQL CPU utilization dropped by 65% because "
                        "unconfirmed hold attempts stayed entirely inside in-memory Redis.</p>"
                    )),
                ],
                "outcomes": [
                    "Zero double bookings registered across 50,000+ test ticket transactions.",
                    "PostgreSQL CPU utilization dropped by 65% because unconfirmed hold attempts stayed entirely inside in-memory Redis.",
                ],
            },
            {
                "slug": "ecommerce",
                "title": "Wagtail CMS Enterprise E-Commerce Platform",
                "seo_title": "Wagtail E-Commerce Case Study — Django & Wagtail CMS | Soyal",
                "search_description": (
                    "Technical Case Study: Headless product hub and content management "
                    "platform built with Wagtail CMS Page Models, StreamFields, and "
                    "WooCommerce API synchronization."
                ),
                "categories": [cms, fullstack],
                "badge_label": "CMS & E-commerce",
                "tech_stack_summary": "Django • Wagtail CMS • WooCommerce",
                "tech_chips": "Wagtail CMS, Django 5, WooCommerce Sync",
                "summary": (
                    "<p>Structuring modular Wagtail Page Models and StreamField components for "
                    "editorial product publishing, automated SEO schemas, and WooCommerce REST "
                    "synchronization.</p>"
                ),
                "programming_language": "Python, Django, Wagtail CMS",
                "featured": True,
                "featured_order": 3,
                "role_label": "Wagtail Lead Developer",
                "core_problem": "Editorial team needed modular blocks without code pushes",
                "solution": "Custom StreamFields + WooCommerce sync webhooks",
                "architecture_highlight": (
                    "Enabled editorial staff to launch custom product landing pages "
                    "in <15 mins with zero dev input."
                ),
                "stats": [
                    {"label": "My Role", "value": "Wagtail Lead Developer"},
                    {"label": "Primary CMS", "value": "Wagtail 5 (Django 5)"},
                    {"label": "Key Feature", "value": "Custom StreamFields"},
                    {"label": "Integration", "value": "WooCommerce REST Sync"},
                ],
                "body": [
                    ("heading", "1. Architectural Goal"),
                    ("paragraph", (
                        "<p>Content managers required a highly flexible content management "
                        "interface where marketing teams could build custom landing pages, "
                        "publish rich product stories, and sync inventory counts without "
                        "requiring code updates from backend developers.</p>"
                    )),
                    ("heading", "2. Wagtail Page Model Implementation"),
                    ("code", {
                        "language": "python",
                        "filename": "",
                        "code": (
                            "# Wagtail ProductPage Model Pattern\n"
                            "class ProductPage(Page):\n"
                            "    sku = models.CharField(max_length=50, unique=True)\n"
                            "    price = models.DecimalField(max_digits=10, decimal_places=2)\n"
                            "    body = StreamField([\n"
                            "        ('hero', blocks.HeroBlock()),\n"
                            "        ('product_specs', blocks.SpecTableBlock()),\n"
                            "        ('gallery', blocks.GalleryGridBlock()),\n"
                            "    ], use_json_field=True)\n\n"
                            "    content_panels = Page.content_panels + [\n"
                            "        FieldPanel('sku'),\n"
                            "        FieldPanel('price'),\n"
                            "        FieldPanel('body'),\n"
                            "    ]"
                        ),
                    }),
                    ("heading", "3. Outcomes"),
                    ("paragraph", (
                        "<p>Empowered non-technical content editors to create bespoke "
                        "marketing pages in under 15 minutes, and reduced API synchronization "
                        "delays with WooCommerce store hooks to under 1.5 seconds per product "
                        "update.</p>"
                    )),
                ],
                "outcomes": [
                    "Empowered non-technical content editors to create bespoke marketing pages in under 15 minutes.",
                    "Reduced API synchronization delays with WooCommerce store hooks to under 1.5 seconds per product update.",
                ],
            },
            {
                "slug": "bidding-platform",
                "title": "Real-Time Auction & Bidding Engine",
                "seo_title": "Real-Time Bidding Engine Case Study — Python & WebSockets | Soyal",
                "search_description": (
                    "Technical Case Study: Real-time auction engine using Python WebSockets, "
                    "sub-second state machine validation, and Redis event channels."
                ),
                "categories": [backend],
                "badge_label": "Real-Time System",
                "tech_stack_summary": "Python • WebSockets • Redis",
                "tech_chips": "Python Asyncio, WebSockets, State Machine",
                "summary": (
                    "<p>Building a sub-second bid validation engine with WebSocket "
                    "broadcasting, state machine rules, and race condition settlement logic.</p>"
                ),
                "programming_language": "Python, Asyncio, WebSockets, Redis",
                "featured": False,
                "featured_order": None,
                "role_label": "Systems Developer",
                "core_problem": "High-frequency race conditions during last-second bids",
                "solution": "Async WebSockets + deterministic state machine validator",
                "stats": [
                    {"label": "My Role", "value": "Real-Time Backend Engineer"},
                    {"label": "Protocol", "value": "WebSockets (WSS)"},
                    {"label": "Latency Goal", "value": "< 50ms Broadcast"},
                    {"label": "State Engine", "value": "Redis Lua Scripts"},
                ],
                "body": [
                    ("heading", "1. Problem Statement"),
                    ("paragraph", (
                        "<p>Online auctions closing in the final 10 seconds experience heavy "
                        "\"sniping\" traffic. When dozens of bids arrive within the same 50ms "
                        "window, the system must deterministically validate bid increments, "
                        "reject stale bids, extend the timer, and broadcast the new highest "
                        "bid to all connected clients.</p>"
                    )),
                    ("heading", "2. Atomic Bid Validation via Redis Lua"),
                    ("code", {
                        "language": "lua",
                        "filename": "",
                        "code": (
                            "-- Redis Lua Script executing atomically on server\n"
                            "local current_bid = tonumber(redis.call('GET', KEYS[1]) or '0')\n"
                            "local new_bid = tonumber(ARGV[1])\n"
                            "local user_id = ARGV[2]\n\n"
                            "if new_bid > current_bid then\n"
                            "  redis.call('SET', KEYS[1], new_bid)\n"
                            "  redis.call('PUBLISH', KEYS[2], cjson.encode({bid = new_bid, user = user_id}))\n"
                            "  return 1\n"
                            "else\n"
                            "  return 0\n"
                            "end"
                        ),
                    }),
                    ("heading", "3. Outcomes"),
                    ("paragraph", (
                        "<p>Achieved atomic sub-10ms bid evaluation using single-threaded Redis "
                        "Lua scripts, maintaining stable WebSocket connection pools across "
                        "2,000+ simultaneous watchers per auction room.</p>"
                    )),
                ],
                "outcomes": [
                    "Achieved atomic sub-10ms bid evaluation using single-threaded Redis Lua scripts.",
                    "Maintained stable WebSocket connection pools across 2,000+ simultaneous watchers per auction room.",
                ],
            },
        ]

        for data in projects:
            categories = data.pop("categories")
            stats = data.pop("stats")
            outcomes = data.pop("outcomes")
            body = data.pop("body")
            slug = data.pop("slug")

            page = upsert_child_page(projects_index, ProjectPage, slug, {**data, "body": body})
            page.categories.set(categories)
            page.save()
            page.save_revision().publish()

            sync_children(page, "stats", stats)
            sync_children(page, "outcomes", [{"text": text} for text in outcomes])

    # ------------------------------------------------------------------
    # Blog
    # ------------------------------------------------------------------
    def _seed_blog_index(self, home):
        return upsert_child_page(home, BlogIndexPage, "blog", {
            "title": "Blog",
            "seo_title": "Engineering Blog & Technical Guides | Soyal",
            "search_description": (
                "In-depth technical articles on Django & Wagtail CMS architecture, "
                "high-concurrency FastAPI lock engines, database optimization, and Laravel REST APIs."
            ),
            "intro_eyebrow": "Wagtail CMS & Backend Engineering Insights",
            "intro_heading": "Engineering Blog & Technical Guides",
            "intro_text": (
                "In-depth technical articles on Django & Wagtail CMS architecture, "
                "high-concurrency FastAPI lock engines, database optimization, and Laravel REST APIs."
            ),
        })

    def _seed_blog_pages(self, blog_index):
        wagtail_cat = BlogCategory.objects.get_or_create(slug="wagtail", defaults={"name": "Django & Wagtail"})[0]
        fastapi_cat = BlogCategory.objects.get_or_create(slug="fastapi", defaults={"name": "FastAPI & Async"})[0]
        database_cat = BlogCategory.objects.get_or_create(slug="database", defaults={"name": "Databases & SQL"})[0]
        laravel_cat = BlogCategory.objects.get_or_create(slug="laravel", defaults={"name": "Laravel"})[0]
        django_cat = BlogCategory.objects.get_or_create(slug="django", defaults={"name": "Django"})[0]

        posts = [
            {
                "slug": "django-wagtail-performance-guide",
                "title": "Optimizing Django & Wagtail CMS for Enterprise Scale: Queries, Caching & StreamFields",
                "seo_title": "Optimizing Django & Wagtail CMS for Enterprise Scale | Soyal",
                "search_description": (
                    "A comprehensive technical guide to structuring Wagtail custom Page Models, "
                    "query profiling, select_related optimizations, and Redis StreamField caching."
                ),
                "categories": [wagtail_cat, django_cat, database_cat],
                "tags": ["django", "wagtail", "orm"],
                "category_label": "Django / Wagtail",
                "excerpt": (
                    "How to structure custom Page Models, avoid N+1 ORM bottlenecks, cache "
                    "StreamField blocks with Redis, and maintain 99+ PageSpeed scores in production."
                ),
                "date_published": "2026-08-12",
                "read_minutes": 8,
                "featured": True,
                "show_toc": True,
                "body": [
                    ("heading", "1. Introduction"),
                    ("paragraph", (
                        "<p>Wagtail CMS is one of the most powerful content management systems "
                        "built on Django. Its authoring interface and flexible StreamField "
                        "blocks allow non-technical marketing teams to compose modular web "
                        "pages without touching code.</p>"
                        "<p>However, when a Wagtail site scales to hundreds of custom Page "
                        "Models, complex StreamFields, images, and foreign key relations, "
                        "performance can rapidly degrade if query optimization and caching are "
                        "overlooked. In this guide, we will break down exact techniques to keep "
                        "response times under 50ms.</p>"
                    )),
                    ("heading", "2. Clean StreamField Architecture"),
                    ("paragraph", (
                        "<p>Always modularize custom StreamField blocks into reusable "
                        "<code>blocks.py</code> definitions rather than bloating model files. "
                        "Here is the recommended pattern:</p>"
                    )),
                    ("code", {
                        "language": "python",
                        "filename": "blocks.py",
                        "code": (
                            "from wagtail import blocks\n"
                            "from wagtail.images.blocks import ImageChooserBlock\n\n"
                            "class HeroBlock(blocks.StructBlock):\n"
                            "    heading = blocks.CharBlock(max_length=100)\n"
                            "    subtitle = blocks.TextBlock(required=False)\n"
                            "    background_image = ImageChooserBlock()\n\n"
                            "    class Meta:\n"
                            "        template = \"blocks/hero_block.html\"\n"
                            "        icon = \"image\""
                        ),
                    }),
                    ("heading", "3. Eliminating N+1 ORM Bottlenecks"),
                    ("paragraph", (
                        "<p>A common issue in Wagtail templates is referencing foreign keys "
                        "(like author profiles or featured images) inside page iteration loops. "
                        "Without prefetching, Django issues a database query per loop "
                        "iteration.</p>"
                    )),
                    ("code", {
                        "language": "python",
                        "filename": "",
                        "code": (
                            "# Optimized get_context query pattern\n"
                            "def get_context(self, request):\n"
                            "    context = super().get_context(request)\n"
                            "    context['articles'] = (\n"
                            "        BlogPage.objects.live()\n"
                            "        .select_related('owner', 'feed_image')\n"
                            "        .prefetch_related('tagged_items__tag')\n"
                            "        .order_by('-first_published_at')[:10]\n"
                            "    )\n"
                            "    return context"
                        ),
                    }),
                    ("heading", "4. Redis Cache Middleware"),
                    ("paragraph", (
                        "<p>By wrapping full Wagtail page renders in Redis template caching, "
                        "server-side render latency drops from ~120ms to &lt;15ms.</p>"
                    )),
                    ("heading", "5. Key Takeaways"),
                    ("bullet_list", [
                        "Modularize StreamFields into distinct block classes with custom template fragments.",
                        "Always override get_context() to apply select_related() and prefetch_related().",
                        "Cache rendered page fragments in Redis for instant client loads.",
                    ]),
                ],
            },
            {
                "slug": "fastapi-redis-locking",
                "title": "Preventing Race Conditions with FastAPI and Redis Distributed Locks",
                "seo_title": "Preventing Race Conditions with FastAPI and Redis Locks | Soyal",
                "search_description": (
                    "Technical guide on high-concurrency ticket reservations, Redis distributed "
                    "lock patterns (NX EX), and atomic Lua script state transitions in FastAPI."
                ),
                "categories": [fastapi_cat, database_cat],
                "tags": ["fastapi", "redis", "concurrency"],
                "category_label": "FastAPI & Async",
                "excerpt": (
                    "Building atomic seat reservations and high-concurrency ticket release "
                    "engines with Redis TTL keys and Python Asyncio."
                ),
                "date_published": "2026-07-28",
                "read_minutes": 6,
                "featured": False,
                "body": [
                    ("heading", "1. The High Concurrency Challenge"),
                    ("paragraph", (
                        "<p>When launching high-demand ticket releases or flash sales, "
                        "thousands of incoming HTTP requests attempt to reserve the exact same "
                        "seat resource simultaneously. Standard SQL UPDATE queries result in "
                        "lock wait timeouts or double-booking race conditions.</p>"
                    )),
                    ("heading", "2. Implementing Redis Key Lock (SET NX EX)"),
                    ("paragraph", (
                        "<p>Using Redis' atomic <code>SET key value NX EX seconds</code> "
                        "command, only the first request acquires the lock key. Subsequent "
                        "requests within the TTL window receive an immediate lock failure "
                        "response without stressing the SQL database.</p>"
                    )),
                    ("code", {
                        "language": "python",
                        "filename": "",
                        "code": (
                            "# Async Redis Lock Acquisition in FastAPI\n"
                            "@router.post(\"/reserve-seat\")\n"
                            "async def reserve_seat(seat_id: str, user_id: int):\n"
                            "    lock_key = f\"lock:seat:{seat_id}\"\n"
                            "    acquired = await redis.set(lock_key, user_id, nx=True, ex=600)\n"
                            "    if not acquired:\n"
                            "        raise HTTPException(status_code=409, detail=\"Seat is currently held by another user\")\n"
                            "    return {\"status\": \"reserved\", \"expires_in_seconds\": 600}"
                        ),
                    }),
                    ("heading", "3. Summary"),
                    ("paragraph", (
                        "<p>Shifting short-lived locks into in-memory Redis drastically "
                        "improves backend throughput and eliminates database contention "
                        "during surge traffic events.</p>"
                    )),
                ],
            },
            {
                "slug": "laravel-pos-database-architecture",
                "title": "Designing High-Concurrency Multi-Tenant Database Schemas in Laravel",
                "seo_title": "Designing Multi-Tenant Database Schemas in Laravel | Soyal",
                "search_description": (
                    "Technical guide on multi-outlet database design, inventory deduction "
                    "isolation using lockForUpdate(), and REST API payload management in Laravel."
                ),
                "categories": [laravel_cat, database_cat],
                "tags": ["laravel", "mysql", "database"],
                "category_label": "Laravel & SQL",
                "excerpt": (
                    "Multi-store inventory deduction, pessimistic row locking (lockForUpdate()), "
                    "and REST payload verification for point-of-sale platforms."
                ),
                "date_published": "2026-07-14",
                "read_minutes": 7,
                "featured": False,
                "body": [
                    ("heading", "1. Multi-Outlet Inventory Isolation"),
                    ("paragraph", (
                        "<p>When a single retail franchise operates multiple store locations, "
                        "product stock must be isolated per outlet while sharing a single "
                        "unified master product catalog.</p>"
                    )),
                    ("heading", "2. Atomic Transactions & Row Locking"),
                    ("paragraph", (
                        "<p>In Laravel, wrapping stock deduction logic in "
                        "<code>DB::transaction()</code> with Eloquent's "
                        "<code>lockForUpdate()</code> prevents concurrent cashier terminals "
                        "from deducting below zero quantity.</p>"
                    )),
                    ("code", {
                        "language": "php",
                        "filename": "",
                        "code": (
                            "// Laravel Eloquent Transaction Pattern\n"
                            "DB::transaction(function () use ($outletId, $items) {\n"
                            "    foreach ($items as $item) {\n"
                            "        $stock = OutletStock::where('outlet_id', $outletId)\n"
                            "            ->where('product_id', $item['product_id'])\n"
                            "            ->lockForUpdate()\n"
                            "            ->firstOrFail();\n\n"
                            "        $stock->decrement('quantity', $item['qty']);\n"
                            "    }\n"
                            "});"
                        ),
                    }),
                    ("heading", "3. Conclusion"),
                    ("paragraph", (
                        "<p>Always leverage explicit relational foreign keys, indexed foreign "
                        "key columns, and pessimistic row locking when engineering commercial "
                        "transaction systems.</p>"
                    )),
                ],
            },
        ]

        for data in posts:
            categories = data.pop("categories")
            tags = data.pop("tags")
            slug = data.pop("slug")
            data["date_published"] = date.fromisoformat(data["date_published"])
            page = upsert_child_page(blog_index, BlogPostPage, slug, data)
            page.categories.set(categories)
            page.tags.set(tags)
            page.save()
            page.save_revision().publish()

    # ------------------------------------------------------------------
    # Contact
    # ------------------------------------------------------------------
    def _seed_contact_page(self, home):
        upsert_child_page(home, ContactPage, "contact", {
            "title": "Contact",
            "seo_title": "Contact Soyal | Backend & Software Developer Kathmandu Nepal",
            "search_description": (
                "Get in touch with Soyal for senior backend developer roles, Python Django "
                "projects, Wagtail CMS engineering, or technical consultation in Kathmandu, Nepal."
            ),
            "intro_eyebrow": "Get In Touch",
            "intro_heading": "Let's Talk Code & Projects",
            "intro_text": (
                "<p>Have a backend project idea, need Wagtail CMS integration, or "
                "want to discuss a senior engineering opportunity? Reach out "
                "directly or fill out the form below.</p>"
            ),
            "direct_heading": "Direct Communication",
            "direct_text": (
                "<p>I prefer direct, clear communication. I am based in "
                "Kathmandu, Nepal (UTC+5:45) and generally respond to all "
                "messages within 24 hours.</p>"
            ),
            "timezone_detail": "Nepal Time (NPT, UTC+5:45) • Available for Remote Teams",
            "success_message": (
                "Thank you! Your message has been sent — I'll get back to you shortly."
            ),
        })

    # ------------------------------------------------------------------
    # Resume
    # ------------------------------------------------------------------
    def _seed_resume_page(self, home):
        resume = upsert_child_page(home, ResumePage, "resume", {
            "title": "Resume",
            "seo_title": "Developer Resume | Soyal Senior Backend Engineer",
            "search_description": (
                "Official technical resume of Soyal — Senior Backend Developer in Kathmandu, "
                "Nepal specializing in Python, Django, Wagtail CMS, FastAPI, and Laravel API architecture."
            ),
            "full_name": "Soyal",
            "tagline": "Senior Backend Developer / Software Engineer",
            "contact_line": "Kathmandu, Nepal • soyal@example.com • https://soyal-portfolio.dev",
            "professional_summary": (
                "<p>Senior Backend Developer with comprehensive experience architecting "
                "production APIs, database schemas, and business applications. Specialized in "
                "Python (Django, FastAPI), Wagtail CMS, PHP (Laravel), and PostgreSQL/MySQL "
                "databases. Focused on maintainability, API security, and database query "
                "optimization.</p>"
            ),
            "education_line": (
                "Bachelor of Science in Computer Science & Information Technology "
                "(BSc.CSIT)"
            ),
            "education_location": "Kathmandu, Nepal",
        })

        sync_children(resume, "skill_categories", [
            {"label": "Languages", "values": "Python, PHP, SQL, JavaScript (ES6+), HTML5, CSS3"},
            {"label": "Frameworks", "values": "Django, FastAPI, Wagtail CMS, Laravel, Vue.js"},
            {"label": "Databases", "values": "PostgreSQL, MySQL, Redis, SQLite"},
            {"label": "Engineering", "values": "REST APIs, OAuth2/JWT, Microservices, Git, Docker"},
        ])
        sync_children(resume, "experience_entries", [
            {
                "title": "Senior Backend Developer — Enterprise Software Solutions",
                "date_range": "2023 — Present",
                "location": "Kathmandu, Nepal (Remote)",
                "bullet_points": (
                    "Designed and shipped high-availability Python REST APIs (Django/FastAPI) "
                    "supporting multi-tenant POS platforms.\n"
                    "Created Wagtail CMS custom page models and StreamField structures for "
                    "content workflow management.\n"
                    "Optimized database queries and index strategies in PostgreSQL, "
                    "eliminating N+1 bottlenecks."
                ),
            },
            {
                "title": "Full-Stack Software Engineer — Web Application Studio",
                "date_range": "2021 — 2023",
                "location": "Kathmandu, Nepal",
                "bullet_points": (
                    "Engineered NexusPOS using Laravel and Vue.js with multi-outlet billing "
                    "and kitchen display system integration.\n"
                    "Integrated payment gateway API webhooks with transaction verification "
                    "and fallback logs."
                ),
            },
        ])
        sync_children(resume, "project_highlights", [
            {"name": "NexusPOS", "description": "Multi-store POS platform built with Laravel, Vue, and MySQL."},
            {"name": "Cinema Ticket Engine", "description": "High-concurrency booking engine using FastAPI and Redis lock keys."},
            {"name": "Wagtail E-Commerce", "description": "Headless Wagtail CMS product hub integrated with Django."},
        ])
