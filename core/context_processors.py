def site_brand(request):
    """Exposes the primary nav pages so header/footer partials can render
    real Wagtail URLs (and highlight the active one) instead of filenames."""
    from about.models import AboutPage
    from blog.models import BlogIndexPage
    from contact.models import ContactPage
    from experience.models import ExperiencePage
    from home.models import HomePage
    from projects.models import ProjectsIndexPage
    from resume.models import ResumePage

    def first(model):
        return model.objects.live().first()

    nav_pages = {
        "home": first(HomePage),
        "about": first(AboutPage),
        "experience": first(ExperiencePage),
        "projects": first(ProjectsIndexPage),
        "blog": first(BlogIndexPage),
        "contact": first(ContactPage),
        "resume": first(ResumePage),
    }

    nav_links = [
        ("Home", nav_pages["home"]),
        ("About", nav_pages["about"]),
        ("Experience", nav_pages["experience"]),
        ("Projects", nav_pages["projects"]),
        ("Blog", nav_pages["blog"]),
        ("Contact", nav_pages["contact"]),
    ]

    return {
        "nav_links": nav_links,
        "nav_pages": nav_pages,
    }
