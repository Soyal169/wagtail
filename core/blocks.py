from django.utils.text import slugify
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from wagtail import blocks


class HeadingBlock(blocks.CharBlock):
    """A single H2 section heading. Anchored with a slugified id so it can be
    linked to from an auto-generated table of contents."""

    class Meta:
        icon = "title"
        template = "core/blocks/heading_block.html"
        label = "Heading"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["anchor_id"] = slugify(value)
        return context


class ParagraphBlock(blocks.RichTextBlock):
    class Meta:
        icon = "pilcrow"
        template = "core/blocks/paragraph_block.html"
        label = "Paragraph"
        features = ["bold", "italic", "link"]


CODE_LANGUAGE_CHOICES = [
    ("python", "Python"),
    ("php", "PHP"),
    ("javascript", "JavaScript"),
    ("sql", "SQL"),
    ("lua", "Lua"),
    ("bash", "Bash / Shell"),
    ("django", "Django template"),
    ("json", "JSON"),
    ("yaml", "YAML"),
]


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=CODE_LANGUAGE_CHOICES, default="python")
    filename = blocks.CharBlock(required=False, max_length=80)
    code = blocks.TextBlock()

    class Meta:
        icon = "code"
        template = "core/blocks/code_block.html"
        label = "Code sample"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        try:
            lexer = get_lexer_by_name(value["language"])
        except ClassNotFound:
            lexer = get_lexer_by_name("text")
        formatter = HtmlFormatter(nowrap=False)
        context["highlighted_code"] = highlight(value["code"], lexer, formatter)
        return context


class BulletListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(blocks.CharBlock(label="Item"), **kwargs)

    class Meta:
        icon = "list-ul"
        template = "core/blocks/bullet_list_block.html"
        label = "Bullet list"


class DiagramNodeBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=80)
    sublabel = blocks.CharBlock(max_length=160, required=False)


class DiagramBlock(blocks.StructBlock):
    """A small left-to-right architecture diagram: a row of labeled boxes
    connected by arrows. Used occasionally in project case studies."""

    nodes = blocks.ListBlock(DiagramNodeBlock())

    class Meta:
        icon = "sitemap"
        template = "core/blocks/diagram_block.html"
        label = "Architecture diagram"


class ArticleBodyBlock(blocks.StreamBlock):
    """Shared StreamField body used by blog posts and project case studies."""

    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    code = CodeBlock()
    bullet_list = BulletListBlock()
    diagram = DiagramBlock()
