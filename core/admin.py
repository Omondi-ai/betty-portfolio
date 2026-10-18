from django.contrib import admin
from .models import (
    SiteProfile,
    HeroStat,
    ExpertiseArea,
    StorySection,
    TimelineEntry,
    ImpactStory,
    EvidenceItem,
    ContactMessage,
)


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StorySection)
class StorySectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not StorySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroStat)
class HeroStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(ExpertiseArea)
class ExpertiseAreaAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ("year_label", "title", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(ImpactStory)
class ImpactStoryAdmin(admin.ModelAdmin):
    list_display = ("title", "frame_shape", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(EvidenceItem)
class EvidenceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_public", "is_published")
    list_filter = ("category", "is_public", "is_published")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, request):
        return False