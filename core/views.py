from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm
from .models import (
    HeroStat,
    ExpertiseArea,
    StorySection,
    TimelineEntry,
    ImpactStory,
    EvidenceItem,
)


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you — your message has been sent.")
            return redirect("home")
        messages.error(request, "Please correct the highlighted fields below.")
    else:
        form = ContactForm()

    context = {
        "stats": HeroStat.objects.filter(is_published=True),
        "expertise": ExpertiseArea.objects.filter(is_published=True),
        "story": StorySection.load(),
        "timeline": TimelineEntry.objects.filter(is_published=True),
        "impact": ImpactStory.objects.filter(is_published=True),
        "evidence": EvidenceItem.objects.filter(
            is_published=True, is_public=True
        ),
        "form": form,
    }
    return render(request, "core/home.html", context)