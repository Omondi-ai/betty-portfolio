from django.db import migrations, models


FRAME_CHOICES = [
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


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_expertise_media"),
    ]

    operations = [
        # ---------- StorySection ----------
        migrations.AddField(
            model_name="storysection",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="story/",
                help_text="Optional. Appears opposite the story text.",
            ),
        ),
        migrations.AddField(
            model_name="storysection",
            name="frame_shape",
            field=models.CharField(
                max_length=20,
                choices=FRAME_CHOICES,
                default="leaf",
                help_text="Shape of the image frame. Only used when an image is present.",
            ),
        ),
        migrations.AddField(
            model_name="storysection",
            name="video_url",
            field=models.URLField(
                blank=True,
                help_text=(
                    "Optional. YouTube, Vimeo, or a direct MP4/WebM link. "
                    "Ignored if an image is uploaded."
                ),
            ),
        ),
        # ---------- TimelineEntry ----------
        migrations.AddField(
            model_name="timelineentry",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="timeline/",
                help_text="Optional. Appears opposite the entry text.",
            ),
        ),
        migrations.AddField(
            model_name="timelineentry",
            name="frame_shape",
            field=models.CharField(
                max_length=20,
                choices=FRAME_CHOICES,
                default="scallop",
                help_text="Shape of the image frame. Only used when an image is present.",
            ),
        ),
        migrations.AddField(
            model_name="timelineentry",
            name="video_url",
            field=models.URLField(
                blank=True,
                help_text=(
                    "Optional. YouTube, Vimeo, or a direct MP4/WebM link. "
                    "Ignored if an image is uploaded."
                ),
            ),
        ),
        # ---------- ImpactStory ----------
        migrations.AddField(
            model_name="impactstory",
            name="video_url",
            field=models.URLField(
                blank=True,
                help_text=(
                    "Optional. YouTube, Vimeo, or a direct MP4/WebM link. "
                    "Ignored if an image is uploaded."
                ),
            ),
        ),
        # ---------- EvidenceItem ----------
        migrations.AddField(
            model_name="evidenceitem",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="evidence/",
                help_text="Optional preview image shown opposite the text.",
            ),
        ),
        migrations.AddField(
            model_name="evidenceitem",
            name="frame_shape",
            field=models.CharField(
                max_length=20,
                choices=FRAME_CHOICES,
                default="circle",
                help_text="Shape of the image frame. Only used when an image is present.",
            ),
        ),
        migrations.AddField(
            model_name="evidenceitem",
            name="video_url",
            field=models.URLField(
                blank=True,
                help_text=(
                    "Optional. YouTube, Vimeo, or a direct MP4/WebM link. "
                    "Ignored if an image is uploaded."
                ),
            ),
        ),
    ]