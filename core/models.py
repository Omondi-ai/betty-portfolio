from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


FRAME_SHAPE_CHOICES = [
    ("circle", "Circle"),
    ("oval", "Oval"),
    ("arch", "Arch"),
    ("petal", "Petal"),
    ("bloom", "Bloom"),
    ("leaf", "Leaf"),
    ("scallop", "Scallop"),
    ("blob", "Blob"),
    ("hexagon", "Hexagon"),
]


class SiteProfile(SingletonModel):
    full_name = models.CharField(max_length=120, default="Betty")
    headline = models.CharField(
        max_length=200,
        default="Researcher · Debater · Mentor",
        help_text="Short tagline shown in the hero eyebrow.",
    )
    hero_statement = models.TextField(
        default="Building bridges through inquiry, leadership, and service.",
        help_text="The large hero sentence. Keep it to one or two lines.",
    )
    intro = models.TextField(
        blank=True,
        help_text="Short paragraph under the headline.",
    )
    portrait = models.ImageField(upload_to="portraits/", blank=True, null=True)
    portrait_frame_shape = models.CharField(
        max_length=20,
        choices=FRAME_SHAPE_CHOICES,
        default="arch",
        help_text="Shape of the hero portrait frame.",
    )
    location = models.CharField(max_length=120, blank=True, default="Kenya")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"


class HeroStat(models.Model):
    value = models.CharField(max_length=20, help_text="e.g. 4+, 2, 1st")
    label = models.CharField(max_length=120, help_text="e.g. Years in scout leadership")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} — {self.label}"


class ExpertiseArea(models.Model):
    icon = models.CharField(max_length=8, default="◎", help_text="A single symbol or emoji.")
    title = models.CharField(max_length=120)
    description = models.TextField(help_text="Rich text is supported.")
    tag = models.CharField(max_length=60, blank=True)
    image = models.ImageField(
        upload_to="expertise/",
        blank=True,
        null=True,
        help_text="Optional. Appears opposite the text and takes the frame shape below.",
    )
    frame_shape = models.CharField(
        max_length=20,
        choices=FRAME_SHAPE_CHOICES,
        default="bloom",
        help_text="Shape of the image frame. Only used when an image is present.",
    )
    video_url = models.URLField(
        blank=True,
        help_text="Optional. YouTube, Vimeo, or a direct MP4/WebM link. Ignored if an image is uploaded.",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class StorySection(SingletonModel):
    label = models.CharField(max_length=80, default="My story")
    heading = models.CharField(max_length=200, default="My story")
    aside_location = models.CharField(max_length=200, blank=True, default="Kenya")
    aside_focus = models.TextField(blank=True, help_text="Focus areas, one per line.")
    aside_current = models.CharField(max_length=200, blank=True)
    aside_also = models.CharField(max_length=200, blank=True)
    body = models.TextField(
        blank=True,
        help_text="Rich text. Separate paragraphs with a blank line.",
    )
    image = models.ImageField(
        upload_to="story/",
        blank=True,
        null=True,
        help_text="Optional. Appears opposite the story text.",
    )
    frame_shape = models.CharField(
        max_length=20,
        choices=FRAME_SHAPE_CHOICES,
        default="leaf",
        help_text="Shape of the image frame. Only used when an image is present.",
    )
    video_url = models.URLField(
        blank=True,
        help_text="Optional. YouTube, Vimeo, or a direct MP4/WebM link. Ignored if an image is uploaded.",
    )

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = "Story section"
        verbose_name_plural = "Story section"


class TimelineEntry(models.Model):
    year_label = models.CharField(max_length=40, help_text="e.g. EARLY, BURUNDI, NOW")
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Rich text is supported.")
    image = models.ImageField(
        upload_to="timeline/",
        blank=True,
        null=True,
        help_text="Optional. Appears opposite the entry text.",
    )
    frame_shape = models.CharField(
        max_length=20,
        choices=FRAME_SHAPE_CHOICES,
        default="scallop",
        help_text="Shape of the image frame. Only used when an image is present.",
    )
    video_url = models.URLField(
        blank=True,
        help_text="Optional. YouTube, Vimeo, or a direct MP4/WebM link. Ignored if an image is uploaded.",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.year_label} — {self.title}"


class ImpactStory(models.Model):
    icon = models.CharField(max_length=8, default="◎")
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Rich text is supported.")
    image = models.ImageField(upload_to="impact/", blank=True, null=True)
    frame_shape = models.CharField(
        max_length=20,
        choices=FRAME_SHAPE_CHOICES,
        default="blob",
        help_text="Shape of the image frame in the public gallery.",
    )
    video_url = models.URLField(
        blank=True,
        help_text="Optional. YouTube, Vimeo, or a direct MP4/WebM link. Ignored if an image is uploaded.",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class EvidenceItem(models.Model):
    CATEGORY_CHOICES = [
        ("certificate", "Certificate"),
        ("publication", "Publication"),
        ("media", "Media"),
        ("testimonial", "Testimonial"),
        ("other", "Other"),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="certificate")
    file = models.FileField(upload_to="evidence/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="evidence/",
        blank=True,
        null=True,
        help_text="Optional preview image shown opposite the text.",
    )
    frame_shape = models.CharField(
        max_length=20,
        choices=FRAME_SHAPE_CHOICES,
        default="circle",
        help_text="Shape of the image frame. Only used when an image is present.",
    )
    video_url = models.URLField(
        blank=True,
        help_text="Optional. YouTube, Vimeo, or a direct MP4/WebM link. Ignored if an image is uploaded.",
    )
    is_public = models.BooleanField(
        default=False,
        help_text="Only tick when it is safe to publish.",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"