import uuid
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    SiteProfile,
    StorySection,
    HeroStat,
    ExpertiseArea,
    TimelineEntry,
    ImpactStory,
    EvidenceItem,
    ContactMessage,
)
from .studio_forms import (
    SiteProfileForm,
    StorySectionForm,
    HeroStatForm,
    ExpertiseAreaForm,
    TimelineEntryForm,
    ImpactStoryForm,
    EvidenceItemForm,
)

MAX_IMAGE_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB


SECTION_CONFIG = {
    "stats": {
        "model": HeroStat,
        "form_class": HeroStatForm,
        "label": "Hero stats",
        "singular": "Stat",
        "icon": "📊",
        "description": "The four numbers that appear under the hero.",
        "list_fields": [("value", "Value"), ("label", "Label")],
    },
    "expertise": {
        "model": ExpertiseArea,
        "form_class": ExpertiseAreaForm,
        "label": "Expertise areas",
        "singular": "Expertise area",
        "icon": "◎",
        "description": "The alternating rows in the 'What I do' section.",
        "list_fields": [("icon", "Icon"), ("title", "Title"), ("tag", "Tag")],
    },
    "timeline": {
        "model": TimelineEntry,
        "form_class": TimelineEntryForm,
        "label": "Journey entries",
        "singular": "Journey entry",
        "icon": "🌱",
        "description": "The milestones in your timeline.",
        "list_fields": [("year_label", "Year"), ("title", "Title")],
    },
    "impact": {
        "model": ImpactStory,
        "form_class": ImpactStoryForm,
        "label": "Impact stories",
        "singular": "Impact story",
        "icon": "✦",
        "description": "The gallery of selected work, with photos and frame shapes.",
        "list_fields": [("icon", "Icon"), ("title", "Title")],
    },
    "evidence": {
        "model": EvidenceItem,
        "form_class": EvidenceItemForm,
        "label": "Evidence",
        "singular": "Evidence item",
        "icon": "📄",
        "description": "Certificates, publications, media, testimonials.",
        "list_fields": [
            ("title", "Title"),
            ("category", "Category"),
            ("is_public", "Public"),
        ],
    },
}


@login_required
def dashboard(request):
    profile = SiteProfile.load()
    story = StorySection.load()

    counts = {
        "stats": HeroStat.objects.filter(is_published=True).count(),
        "expertise": ExpertiseArea.objects.filter(is_published=True).count(),
        "timeline": TimelineEntry.objects.filter(is_published=True).count(),
        "impact": ImpactStory.objects.filter(is_published=True).count(),
        "evidence": EvidenceItem.objects.filter(is_published=True).count(),
        "messages_unread": ContactMessage.objects.filter(is_read=False).count(),
        "messages_total": ContactMessage.objects.count(),
    }

    completion = [
        ("Add a portrait photo", bool(profile.portrait)),
        ("Write your hero statement", bool(profile.hero_statement)),
        ("Write your story", bool(story.body)),
        ("Add at least one hero stat", counts["stats"] > 0),
        ("Add at least one expertise area", counts["expertise"] > 0),
        ("Add at least one journey entry", counts["timeline"] > 0),
        ("Add at least one impact story", counts["impact"] > 0),
        ("Upload at least one evidence item", counts["evidence"] > 0),
    ]
    done_count = sum(1 for _, ok in completion if ok)
    total = len(completion)

    return render(
        request,
        "studio/dashboard.html",
        {
            "profile": profile,
            "counts": counts,
            "completion": completion,
            "done_count": done_count,
            "completion_total": total,
            "completion_percent": int((done_count / total) * 100) if total else 0,
            "recent_messages": ContactMessage.objects.all()[:5],
        },
    )


@login_required
def profile_edit(request):
    profile = SiteProfile.load()
    if request.method == "POST":
        form = SiteProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("studio:dashboard")
    else:
        form = SiteProfileForm(instance=profile)

    preview_url = ""
    if profile.portrait:
        try:
            preview_url = profile.portrait.url
        except (ValueError, AttributeError):
            preview_url = ""

    return render(
        request,
        "studio/profile_edit.html",
        {
            "form": form,
            "profile": profile,
            "preview_image_url": preview_url,
            "current_shape": profile.portrait_frame_shape or "arch",
        },
    )


@login_required
def story_edit(request):
    story = StorySection.load()
    if request.method == "POST":
        form = StorySectionForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            form.save()
            messages.success(request, "Your story has been updated.")
            return redirect("studio:dashboard")
    else:
        form = StorySectionForm(instance=story)

    preview_url = ""
    if story.image:
        try:
            preview_url = story.image.url
        except (ValueError, AttributeError):
            preview_url = ""

    return render(
        request,
        "studio/story_edit.html",
        {
            "form": form,
            "story": story,
            "preview_image_url": preview_url,
            "current_shape": story.frame_shape or "leaf",
        },
    )


def _config(section):
    return SECTION_CONFIG.get(section)


@login_required
def section_list(request, section):
    config = _config(section)
    if not config:
        return redirect("studio:dashboard")

    show = request.GET.get("show", "published")
    qs = config["model"].objects.all()
    if show == "hidden":
        qs = qs.filter(is_published=False)
    elif show == "all":
        pass
    else:
        qs = qs.filter(is_published=True)
    items = qs.order_by("order", "id")

    return render(
        request,
        "studio/object_list.html",
        {"section": section, "config": config, "items": items, "show": show},
    )


@login_required
def section_create(request, section):
    config = _config(section)
    if not config:
        return redirect("studio:dashboard")
    FormClass = config["form_class"]

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            last = config["model"].objects.order_by("-order").first()
            if last and last.order >= obj.order:
                obj.order = last.order + 1
            obj.save()
            messages.success(request, f"{config['singular']} added.")
            return redirect("studio:section_list", section=section)
    else:
        form = FormClass()

    return render(
        request,
        "studio/object_form.html",
        {
            "form": form,
            "section": section,
            "config": config,
            "mode": "create",
            "preview_image_url": "",
            "current_shape": "bloom",
        },
    )


@login_required
def section_edit(request, section, pk):
    config = _config(section)
    if not config:
        return redirect("studio:dashboard")
    FormClass = config["form_class"]
    obj = get_object_or_404(config["model"], pk=pk)

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{config['singular']} updated.")
            return redirect("studio:section_list", section=section)
    else:
        form = FormClass(instance=obj)

    preview_url = ""
    for attr in ("image", "portrait"):
        f = getattr(obj, attr, None)
        if f and hasattr(f, "url"):
            try:
                preview_url = f.url
                break
            except (ValueError, AttributeError):
                continue

    current_shape = (
        getattr(obj, "frame_shape", "")
        or getattr(obj, "portrait_frame_shape", "")
        or "bloom"
    )

    return render(
        request,
        "studio/object_form.html",
        {
            "form": form,
            "section": section,
            "config": config,
            "mode": "edit",
            "obj": obj,
            "preview_image_url": preview_url,
            "current_shape": current_shape,
        },
    )


@login_required
@require_POST
def section_delete(request, section, pk):
    config = _config(section)
    if not config:
        return redirect("studio:dashboard")
    obj = get_object_or_404(config["model"], pk=pk)
    obj.is_published = False
    obj.save()
    messages.success(
        request,
        f"{config['singular']} hidden. Restore it from the Hidden tab whenever you like.",
    )
    return redirect("studio:section_list", section=section)


@login_required
@require_POST
def section_restore(request, section, pk):
    config = _config(section)
    if not config:
        return redirect("studio:dashboard")
    obj = get_object_or_404(config["model"], pk=pk)
    obj.is_published = True
    obj.save()
    messages.success(request, f"{config['singular']} restored.")
    return redirect(f"/studio/{section}/?show=hidden")


@login_required
@require_POST
def section_move(request, section, pk, direction):
    config = _config(section)
    if not config:
        return redirect("studio:dashboard")
    model = config["model"]

    items = list(model.objects.order_by("order", "id"))
    if len(items) < 2:
        return redirect("studio:section_list", section=section)

    obj = get_object_or_404(model, pk=pk)
    try:
        idx = items.index(obj)
    except ValueError:
        return redirect("studio:section_list", section=section)

    new_idx = idx - 1 if direction == "up" else idx + 1
    if new_idx < 0 or new_idx >= len(items):
        return redirect("studio:section_list", section=section)

    for i, item in enumerate(items):
        if item.order != i + 1:
            item.order = i + 1
            item.save(update_fields=["order"])

    obj.order = new_idx + 1
    neighbour = items[new_idx]
    neighbour.order = idx + 1
    obj.save(update_fields=["order"])
    neighbour.save(update_fields=["order"])

    return redirect("studio:section_list", section=section)


@login_required
def messages_list(request):
    msgs = ContactMessage.objects.all()
    return render(request, "studio/messages_list.html", {"messages_list": msgs})


@login_required
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=["is_read"])
    return render(request, "studio/message_detail.html", {"message_obj": msg})


@login_required
@require_POST
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, "Message deleted.")
    return redirect("studio:messages_list")


@login_required
@require_POST
def upload_image(request):
    file = request.FILES.get("image")
    if not file:
        return JsonResponse({"error": "No image provided."}, status=400)
    if not file.content_type.startswith("image/"):
        return JsonResponse({"error": "Only image files are allowed."}, status=400)
    if file.size > MAX_IMAGE_UPLOAD_BYTES:
        mb = MAX_IMAGE_UPLOAD_BYTES // (1024 * 1024)
        return JsonResponse({"error": f"Image is larger than {mb} MB."}, status=400)

    ext = Path(file.name).suffix.lower() or ".jpg"
    name = f"uploads/{uuid.uuid4().hex}{ext}"
    saved_path = default_storage.save(name, file)
    return JsonResponse({"url": default_storage.url(saved_path)})