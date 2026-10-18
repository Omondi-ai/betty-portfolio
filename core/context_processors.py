from .models import SiteProfile, ContactMessage


def site_profile(request):
    return {"profile": SiteProfile.load()}


def studio_context(request):
    if not request.path.startswith("/studio/"):
        return {}
    if not request.user.is_authenticated:
        return {}
    return {
        "studio_unread_messages": ContactMessage.objects.filter(is_read=False).count(),
    }