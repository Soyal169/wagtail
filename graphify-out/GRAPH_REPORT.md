# Graph Report - .  (2026-08-18)

## Corpus Check
- 149 files · ~56,269 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 382 nodes · 413 edges · 100 communities (70 shown, 30 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Wagtail Page Hierarchy & Core Models
- Static Prototype Articles & Portfolio Content
- Page Templates & StreamField Blocks
- Database Seeding & Demo Commands
- Home Page & Expertise Pillars
- Home Page & Expertise Pillars
- Frontend Build & Tooling Config
- Contact Form & Admin Workflow
- Custom Template Tags & Filters
- StreamField Custom Blocks
- About Page Data Models
- Python Package Dependencies
- Contact Form & Admin Workflow
- Theme Switching & Client Scripts
- Theme Switching & Client Scripts
- Database Seeding & Demo Commands
- Search View & Query Routing
- Experience & Career History
- Home Page & Expertise Pillars
- Project Portfolio Models
- about/apps Subsystem
- blog/apps Subsystem
- contact/apps Subsystem
- core/apps Subsystem
- Experience & Career History
- home/apps Subsystem
- manage Subsystem
- Project Portfolio Models
- Resume Page & Credentials
- Layout Partials & Meta Tags
- Theme Switching & Client Scripts
- Database Schema Migrations (33)
- Database Schema Migrations (34)
- Database Schema Migrations (35)
- Database Schema Migrations (36)
- Database Schema Migrations (37)
- Database Schema Migrations (38)
- Database Schema Migrations (39)
- Site Settings & Global Configuration
- Experience & Career History
- Database Schema Migrations (42)
- Home Page & Expertise Pillars
- Project Portfolio Models
- Project Portfolio Models
- Resume Page & Credentials
- Resume Page & Credentials
- Project Portfolio Models
- Layout Partials & Meta Tags

## God Nodes (most connected - your core abstractions)
1. `Base Layout Template` - 16 edges
2. `ArticleBodyBlock` - 15 edges
3. `Command` - 14 edges
4. `upsert_child_page()` - 9 edges
5. `HomePage` - 8 edges
6. `Project Python Dependencies` - 8 edges
7. `Breadcrumbs Partial Template` - 8 edges
8. `ContactForm` - 7 edges
9. `ContactSubmission` - 7 edges
10. `sync_children()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Favicon SVG (Prototype)` --semantically_similar_to--> `Favicon SVG (Core)`  [INFERRED] [semantically similar]
  static_prototype/assets/icons/favicon.svg → core/static/icons/favicon.svg
- `Command` --uses--> `AboutPage`  [INFERRED]
  core/management/commands/seed_demo_data.py → about/models.py
- `Meta` --uses--> `ArticleBodyBlock`  [INFERRED]
  blog/models.py → core/blocks.py
- `Meta` --uses--> `ArticleBodyBlock`  [INFERRED]
  projects/models.py → core/blocks.py
- `Profile Image (Soyal Portrait)` --references--> `_seed_portrait()`  [EXTRACTED]
  static_prototype/assets/images/profile.jpg → core/management/commands/seed_demo_data.py

## Import Cycles
- None detected.

## Communities (100 total, 30 thin omitted)

### Community 0 - "Wagtail Page Hierarchy & Core Models"
Cohesion: 0.07
Nodes (32): AboutPage, Page, BlogCategory, BlogIndexPage, BlogPostPage, BlogPostPageTag, Meta, Page (+24 more)

### Community 1 - "Static Prototype Articles & Portfolio Content"
Cohesion: 0.09
Nodes (29): Developer Background & Engineering Principles, About Me Prototype Page, Technical Skills Inventory & Domain Capabilities, Optimizing Django & Wagtail CMS for Enterprise Scale Article, Django ORM Eager Loading and N+1 Elimination, StreamField High-Performance Architecture, Preventing Race Conditions with FastAPI & Redis Distributed Locks Article, Redis Distributed Mutex Locking Pattern (SET NX EX) (+21 more)

### Community 2 - "Page Templates & StreamField Blocks"
Cohesion: 0.11
Nodes (28): About Page Template, Blog Index Page Template, Blog Post Page Template, Contact Page Template, Bullet List StreamField Block Template, Code Highlight StreamField Block Template, System Flow Diagram StreamField Block Template, Heading StreamField Block Template (+20 more)

### Community 3 - "Database Seeding & Demo Commands"
Cohesion: 0.30
Nodes (5): BaseCommand, Command, Idempotent child-row sync: these are presentation-only rows with no independent…, sync_children(), upsert_child_page()

### Community 4 - "Home Page & Expertise Pillars"
Cohesion: 0.20
Nodes (12): Migration, HomePageExpertisePillar, HomePageInterest, HomePagePhilosophyStep, HomePageSnapshotFact, HomePageStatusCard, HomePageStoryBullet, HomePageTerminalRow (+4 more)

### Community 5 - "Home Page & Expertise Pillars"
Cohesion: 0.16
Nodes (8): HomePage, Page, HomeSetUpTests, HomeTests, Tests for homepage functionality and rendering., Create a homepage instance for testing., Tests for basic page structure setup and HomePage creation., WagtailPageTestCase

### Community 6 - "Frontend Build & Tooling Config"
Cohesion: 0.14
Nodes (13): autoprefixer, devDependencies, autoprefixer, postcss, tailwindcss, tailwindcss, name, private (+5 more)

### Community 7 - "Contact Form & Admin Workflow"
Cohesion: 0.22
Nodes (8): ContactSubmissionAdmin, ContactForm, ContactPage, ContactSubmission, Meta, Page, A record of every contact form submission, kept for reference alongside the…, register

### Community 8 - "Custom Template Tags & Filters"
Cohesion: 0.19
Nodes (13): highlight_gradient(), nav_is_active(), Splits a comma-separated CharField value into a trimmed list, e.g. for…, Whether a header nav link should render as the active page. Home matches only…, Wraps the first occurrence of `highlight` within `full_text` in the site's…, Strips a leading http(s):// and any trailing slash for display, e.g.…, Collects (anchor_id, text) tuples for every heading block in a StreamField…, split() (+5 more)

### Community 9 - "StreamField Custom Blocks"
Cohesion: 0.20
Nodes (8): BulletListBlock, CodeBlock, DiagramBlock, HeadingBlock, Meta, ParagraphBlock, A single H2 section heading. Anchored with a slugified id so it can be linked…, A small left-to-right architecture diagram: a row of labeled boxes connected by…

### Community 10 - "About Page Data Models"
Cohesion: 0.39
Nodes (6): AboutPageChecklistItem, AboutPageNarrativeBlock, AboutPageQuickFact, AboutPageSkillCategory, AboutPageWorkspaceRow, Orderable

### Community 11 - "Python Package Dependencies"
Cohesion: 0.25
Nodes (8): Django Package Requirement, django-environ Package Requirement, django-filter Package Requirement, django-taggit Package Requirement, psycopg binary Package Requirement, Project Python Dependencies, Wagtail Package Requirement, whitenoise Package Requirement

### Community 12 - "Contact Form & Admin Workflow"
Cohesion: 0.33
Nodes (5): BaseSiteSetting, Meta, Site-wide brand, contact, and structured-data defaults editable from the admin., SiteBrandSettings, register_setting

### Community 13 - "Theme Switching & Client Scripts"
Cohesion: 0.47
Nodes (3): applyTheme(), initThemeToggle(), updateToggleButtons()

### Community 14 - "Theme Switching & Client Scripts"
Cohesion: 0.47
Nodes (3): applyTheme(), initThemeToggle(), updateToggleButtons()

### Community 15 - "Database Seeding & Demo Commands"
Cohesion: 0.50
Nodes (5): Idempotent by title: loads the prototype's portrait photo into a Wagtail Image…, _seed_portrait(), Favicon SVG (Core), Favicon SVG (Prototype), Profile Image (Soyal Portrait)

### Community 30 - "Layout Partials & Meta Tags"
Cohesion: 0.67
Nodes (3): HTML Head Meta & SEO Partial Template, Schema.org BreadcrumbList JSON-LD Partial Template, Schema.org Person and WebSite JSON-LD Partial Template

### Community 31 - "Theme Switching & Client Scripts"
Cohesion: 0.67
Nodes (3): Dynamic Wagtail Navigation System, Header & Primary Navigation Partial Template, Immediate Theme Detection Script Partial Template

## Knowledge Gaps
- **65 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+60 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HomePage` connect `Home Page & Expertise Pillars` to `Wagtail Page Hierarchy & Core Models`, `Home Page & Expertise Pillars`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `Command` connect `Database Seeding & Demo Commands` to `Wagtail Page Hierarchy & Core Models`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `ArticleBodyBlock` (e.g. with `BlogCategory` and `BlogIndexPage`) actually correct?**
  _`ArticleBodyBlock` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Migration`, `Migration`, `Migration` to the rest of the system?**
  _65 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Wagtail Page Hierarchy & Core Models` be split into smaller, more focused modules?**
  _Cohesion score 0.06914893617021277 - nodes in this community are weakly interconnected._
- **Should `Static Prototype Articles & Portfolio Content` be split into smaller, more focused modules?**
  _Cohesion score 0.08620689655172414 - nodes in this community are weakly interconnected._
- **Should `Page Templates & StreamField Blocks` be split into smaller, more focused modules?**
  _Cohesion score 0.10846560846560846 - nodes in this community are weakly interconnected._