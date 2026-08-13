from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from core.blocks import ArticleBodyBlock


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)

    panels = [FieldPanel("name"), FieldPanel("slug")]

    class Meta:
        verbose_name_plural = "Blog categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPostPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogPostPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BlogIndexPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPostPage"]

    intro_eyebrow = models.CharField(max_length=80, default="Engineering Notes")
    intro_heading = models.CharField(max_length=160, default="Backend & CMS Engineering Blog")
    intro_text = models.TextField(
        default="Deep dives into the problems I've solved building APIs, CMS platforms, and data-driven systems."
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_eyebrow"),
        FieldPanel("intro_heading"),
        FieldPanel("intro_text"),
    ]

    def get_context(self, request, *args, **kwargs):
        # Category narrowing happens in the template (marking non-matching
        # cards `hidden`), not in this queryset, so that every category's
        # cards are present in the DOM for blog.js's instant client-side
        # re-filtering — the same server-rendered page works with or
        # without JS, it just needs a `?category=` link to reload from.
        context = super().get_context(request, *args, **kwargs)
        posts = BlogPostPage.objects.live().child_of(self).order_by("-date_published")

        query = request.GET.get("q", "").strip()
        if query:
            posts = posts.filter(
                Q(title__icontains=query) | Q(excerpt__icontains=query)
            ).distinct()

        category_slug = request.GET.get("category") or "all"

        context["featured_post"] = (
            None
            if query
            else BlogPostPage.objects.live().child_of(self).filter(featured=True).order_by("-date_published").first()
        )

        paginator = Paginator(posts, 9)
        page_number = request.GET.get("page")
        context["posts_page"] = paginator.get_page(page_number)
        context["categories"] = BlogCategory.objects.all()
        context["active_category"] = category_slug
        context["search_query"] = query
        return context


class BlogPostPage(Page):
    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    categories = ParentalManyToManyField(BlogCategory, related_name="posts")
    tags = ClusterTaggableManager(through=BlogPostPageTag, blank=True)

    category_label = models.CharField(
        max_length=80, help_text="Human-readable badge shown on the card, e.g. 'FastAPI & Async'"
    )
    excerpt = models.TextField(max_length=400)
    date_published = models.DateField()
    read_minutes = models.PositiveIntegerField(default=5)
    featured = models.BooleanField(default=False)

    body = StreamField(ArticleBodyBlock(), blank=True, use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField("excerpt"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("categories"),
        FieldPanel("tags"),
        FieldPanel("category_label"),
        FieldPanel("excerpt"),
        FieldPanel("date_published"),
        FieldPanel("read_minutes"),
        FieldPanel("featured"),
        FieldPanel("body"),
    ]

    @property
    def category_slugs(self):
        return " ".join(self.categories.values_list("slug", flat=True))

    @property
    def heading_count(self):
        return sum(1 for block in self.body if block.block_type == "heading")
