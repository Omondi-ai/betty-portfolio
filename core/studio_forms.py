from django import forms
from django.utils.safestring import mark_safe

from .models import (
    SiteProfile,
    StorySection,
    HeroStat,
    ExpertiseArea,
    TimelineEntry,
    ImpactStory,
    EvidenceItem,
    FRAME_SHAPE_CHOICES,
)
from .utils import clean_html, clean_inline


class QuillTextarea(forms.Textarea):
    """A textarea that JavaScript upgrades into a Quill editor.

    Pass inline=True for short, headline-style fields — the editor then
    exposes only bold, italic, underline, and links, and stores inline-only HTML.
    """

    def __init__(self, attrs=None, inline=False):
        default = {"data-quill": "true", "rows": 10, "class": "quill-source"}
        if inline:
            default["data-quill-inline"] = "true"
        if attrs:
            default.update(attrs)
        super().__init__(default)


class ShapePickerWidget(forms.Widget):
    """Renders the nine frame shapes as visual radio tiles."""

    def render(self, name, value, attrs=None, renderer=None):
        parts = ['<div class="shape-picker" role="radiogroup">']
        for key, label in FRAME_SHAPE_CHOICES:
            checked = "checked" if str(value) == key else ""
            parts.append(
                f'<label class="shape-option" title="{label}">'
                f'<input type="radio" name="{name}" value="{key}" {checked}>'
                f'<span class="shape-option-preview">'
                f'<span class="shape-fill shape-{key}"></span>'
                f'</span>'
                f'<span class="shape-option-label">{label}</span>'
                f'</label>'
            )
        parts.append("</div>")
        return mark_safe("".join(parts))


class BaseRichForm(forms.ModelForm):
    """Sanitises every field listed in `rich_fields` on clean."""

    rich_fields = []

    def clean(self):
        cleaned = super().clean()
        for field_name in self.rich_fields:
            if field_name in cleaned:
                cleaned[field_name] = clean_html(cleaned[field_name])
        return cleaned


class SiteProfileForm(BaseRichForm):
    rich_fields = []

    class Meta:
        model = SiteProfile
        fields = [
            "full_name",
            "headline",
            "hero_statement",
            "intro",
            "portrait",
            "portrait_frame_shape",
            "location",
            "email",
            "phone",
            "linkedin_url",
            "cv_file",
        ]
        widgets = {
            "hero_statement": QuillTextarea(attrs={"rows": 3}, inline=True),
            "intro": QuillTextarea(attrs={"rows": 4}, inline=True),
            "portrait_frame_shape": ShapePickerWidget(),
        }

    def clean_hero_statement(self):
        return clean_inline(self.cleaned_data.get("hero_statement", ""))

    def clean_intro(self):
        return clean_inline(self.cleaned_data.get("intro", ""))


class StorySectionForm(BaseRichForm):
    rich_fields = ["body"]

    class Meta:
        model = StorySection
        fields = [
            "label",
            "heading",
            "aside_location",
            "aside_focus",
            "aside_current",
            "aside_also",
            "body",
        ]
        widgets = {
            "body": QuillTextarea(attrs={"rows": 14}),
            "aside_focus": forms.Textarea(attrs={"rows": 3}),
        }


class HeroStatForm(forms.ModelForm):
    class Meta:
        model = HeroStat
        fields = ["value", "label", "order", "is_published"]


class ExpertiseAreaForm(BaseRichForm):
    rich_fields = ["description"]

    class Meta:
        model = ExpertiseArea
        fields = [
            "icon",
            "title",
            "description",
            "tag",
            "image",
            "frame_shape",
            "video_url",
            "order",
            "is_published",
        ]
        widgets = {
            "description": QuillTextarea(attrs={"rows": 6}),
            "frame_shape": ShapePickerWidget(),
        }


class TimelineEntryForm(BaseRichForm):
    rich_fields = ["description"]

    class Meta:
        model = TimelineEntry
        fields = ["year_label", "title", "description", "order", "is_published"]
        widgets = {
            "description": QuillTextarea(attrs={"rows": 5}),
        }


class ImpactStoryForm(BaseRichForm):
    rich_fields = ["description"]

    class Meta:
        model = ImpactStory
        fields = [
            "icon",
            "title",
            "description",
            "image",
            "frame_shape",
            "order",
            "is_published",
        ]
        widgets = {
            "description": QuillTextarea(attrs={"rows": 6}),
            "frame_shape": ShapePickerWidget(),
        }


class EvidenceItemForm(BaseRichForm):
    rich_fields = ["description"]

    class Meta:
        model = EvidenceItem
        fields = [
            "title",
            "category",
            "file",
            "external_url",
            "description",
            "is_public",
            "order",
            "is_published",
        ]
        widgets = {
            "description": QuillTextarea(attrs={"rows": 4}),
        }