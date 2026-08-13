from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from about.models import AboutPage, AboutPageChecklistItem, AboutPageQuickFact, AboutPageSkillCategory
from blog.models import BlogCategory, BlogIndexPage, BlogPostPage
from contact.models import ContactPage
from core.models import SiteBrandSettings
from experience.models import ExperiencePage, ExperienceEntry
from home.models import HomePage, HomePagePhilosophyStep
from projects.models import ProjectCategory, ProjectsIndexPage, ProjectPage, ProjectOutcome, ProjectStat
from resume.models import (
    ResumePage,
    ResumeExperienceEntry,
    ResumeProjectHighlight,
    ResumeSkillCategory,
)
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
        brand.tagline = "Senior Backend Developer & Software Engineer"
        brand.footer_blurb = (
            "Senior Backend Developer & Software Engineer based in Kathmandu, Nepal. "
            "Building production backend systems with Django, Wagtail, FastAPI, and Laravel."
        )
        brand.location = "Kathmandu, Nepal"
        brand.availability_status = "Available for Senior Backend & Software Engineering Roles"
        brand.contact_email = "soyal@example.com"
        brand.github_url = "https://github.com/"
        brand.linkedin_url = "https://linkedin.com/in/"
        brand.person_name = "Soyal"
        brand.person_job_title = "Senior Backend Developer"
        brand.knows_about = (
            "Python, Django, FastAPI, PHP, Laravel, Wagtail CMS, REST APIs, MySQL, "
            "PostgreSQL, Database Design, API Security"
        )
        brand.org_name = "Independent Engineering Consultant"
        brand.save()

    # ------------------------------------------------------------------
    # Home
    # ------------------------------------------------------------------
    def _seed_home_page(self, site):
        home = site.root_page.specific
        if not isinstance(home, HomePage):
            raise RuntimeError("Expected the site root page to be a HomePage.")

        home.title = "Home"
        home.seo_title = "Backend Developer & Software Engineer in Nepal | Soyal"
        home.search_description = (
            "Senior Backend Developer in Kathmandu, Nepal specializing in Python, Django, "
            "FastAPI, Laravel, REST API architecture, and Wagtail CMS solutions."
        )
        home.hero_heading_main = (
            "Backend Developer building reliable APIs & production systems."
        )
        home.hero_heading_highlight = "reliable APIs"
        home.hero_subhead = (
            "I specialize in Python, Django, FastAPI, PHP, Laravel, and Wagtail CMS. Based in "
            "Kathmandu, Nepal, I architect robust database models, high-performance REST APIs, "
            "and scalable business logic for real-world application platforms."
        )
        home.skill_pills = (
            "Python, Django, FastAPI, Laravel, Wagtail CMS, MySQL / PostgreSQL, REST APIs"
        )
        home.terminal_json = {
            "identity": {
                "name": "Soyal",
                "role": "Senior Backend Engineer",
                "location": "Kathmandu, Nepal",
                "status": "Open to Remote / Global Roles",
            },
            "services": [
                "REST API Architecture",
                "Wagtail / Django Enterprise CMS",
                "Database Design & Query Optimization",
                "Authentication & Payment Security",
            ],
            "metrics": {
                "uptime": "99.98%",
                "latency": "24ms",
                "note": "Clean Architecture",
            },
        }
        home.featured_projects_eyebrow = "Case Studies"
        home.featured_projects_heading = "Featured Engineering Projects"
        home.featured_projects_intro = (
            "Production business software, POS systems, booking engines, and API "
            "infrastructure built with Django, Laravel, and Wagtail."
        )
        home.philosophy_eyebrow = "Engineering Philosophy"
        home.philosophy_heading = "How I Build Software"
        home.philosophy_intro = (
            "A systematic approach to architecting backend systems that remain "
            "maintainable, secure, and performant over time."
        )
        home.contact_cta_heading = "Have a problem worth solving?"
        home.contact_cta_text = (
            "<p>I'm actively interested in senior backend engineering roles, Django/Wagtail "
            "CMS developments, and complex software projects.</p>"
        )
        home.save()
        home.save_revision().publish()

        sync_children(home, "philosophy_steps", [
            {
                "number": "01",
                "title": "Understand & Model",
                "description": (
                    "Deeply analyze domain logic before writing code. Design clear database "
                    "schemas, relational foreign keys, and API contracts."
                ),
            },
            {
                "number": "02",
                "title": "Secure & Authorize",
                "description": (
                    "Implement strict role-based authorization (RBAC), JWT / Session "
                    "security, payload validation, and SQL injection prevention by default."
                ),
            },
            {
                "number": "03",
                "title": "Optimize & Maintain",
                "description": (
                    "Benchmark database query execution times, eliminate N+1 queries, add "
                    "Redis caching, and write clean, modular Django/Wagtail code."
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
            "seo_title": "About Soyal | Senior Backend & Wagtail Developer in Kathmandu Nepal",
            "search_description": (
                "Learn about Soyal's background as a Senior Backend Developer specializing in "
                "Python, Django, Wagtail CMS, Laravel REST APIs, and database architecture in Nepal."
            ),
            "intro_heading": "Engineering robust backend platforms with business clarity.",
            "intro_text": (
                "<p>I am a Senior Backend Developer & Software Engineer based in Kathmandu, "
                "Nepal. My work focuses on building maintainable REST APIs, enterprise content "
                "management systems with Wagtail/Django, and business operations platforms.</p>"
            ),
            "bio_heading": "Professional Background & Value",
            "bio_paragraph_1": (
                "<p>In software development, visual design gets immediate attention, but "
                "backend architecture determines long-term stability. I specialize in designing "
                "the core engines that power applications — relational database models, secure "
                "authentication flows, background queues, and API gateways.</p>"
            ),
            "bio_paragraph_2": (
                "<p>My primary technology focus centers around <strong>Python (Django, FastAPI, "
                "Wagtail CMS)</strong> and <strong>PHP (Laravel)</strong>, backed by relational "
                "databases like <strong>MySQL</strong> and <strong>PostgreSQL</strong>. Having "
                "built production Point-of-Sale (POS) systems, cinema ticketing engines, and "
                "enterprise e-commerce platforms, I design systems with high maintainability and "
                "security in mind.</p>"
            ),
            "mindset_heading": "Engineering Mindset",
            "mindset_text": (
                "<p>I prioritize clean domain modeling before writing code. A well-designed "
                "database schema prevents hundreds of refactoring hours down the road. Every "
                "endpoint I ship includes proper payload validation, explicit error handling, "
                "structured logging, and non-blocking query execution.</p>"
            ),
            "quick_facts_heading": "Quick Facts",
            "capabilities_eyebrow": "Technical Skill Inventory",
            "capabilities_heading": "Technologies & Capabilities",
        })

        sync_children(about, "checklist_items", [
            {"text": "Django & Wagtail CMS"},
            {"text": "FastAPI Async REST APIs"},
            {"text": "Laravel Enterprise Backend"},
            {"text": "Relational Database Design"},
            {"text": "Redis Caching & Lock Engines"},
            {"text": "API Security & Role RBAC"},
        ])
        sync_children(about, "quick_facts", [
            {"label": "Primary Location", "value": "Kathmandu, Nepal"},
            {"label": "Primary Specialization", "value": "Backend Architecture & CMS"},
            {"label": "Core Languages", "value": "Python, PHP, JavaScript, SQL"},
            {"label": "Availability", "value": "Senior Backend & Remote Roles"},
        ])
        sync_children(about, "skill_categories", [
            {
                "badge": "BE",
                "title": "Backend Engineering",
                "items": (
                    "<ul><li>Python (Django, FastAPI)</li><li>PHP (Laravel)</li>"
                    "<li>RESTful API Design & Specification</li><li>JWT & OAuth Authentication</li>"
                    "<li>Background Workers & Queues</li></ul>"
                ),
            },
            {
                "badge": "DB",
                "title": "Databases & Caching",
                "items": (
                    "<ul><li>PostgreSQL & MySQL</li><li>Relational Database Design</li>"
                    "<li>Index Optimization & EXPLAIN</li><li>Redis Caching & Lock Engines</li>"
                    "<li>SQLite for Embedded Systems</li></ul>"
                ),
            },
            {
                "badge": "CMS",
                "title": "CMS & Content Platforms",
                "items": (
                    "<ul><li>Wagtail CMS (Page Models, StreamField)</li>"
                    "<li>Django Admin Customization</li><li>WordPress & WooCommerce Backend</li>"
                    "<li>Headless Content Delivery</li><li>HTML5 / Tailwind CSS / Vanilla JS</li></ul>"
                ),
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
            "intro_heading": "Direct Contact Details",
            "intro_text": (
                "<p>I am located in Kathmandu, Nepal (UTC+5:45) and regularly collaborate with "
                "remote engineering teams worldwide.</p>"
            ),
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
                "(BSc.CSIT) — Kathmandu, Nepal"
            ),
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
