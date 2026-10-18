from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="expertisearea",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text=(
                    "Optional. If provided, it appears opposite the text "
                    "and takes the frame shape below."
                ),
                null=True,
                upload_to="expertise/",
            ),
        ),
        migrations.AddField(
            model_name="expertisearea",
            name="frame_shape",
            field=models.CharField(
                choices=[
                    ("circle", "Circle"),
                    ("oval", "Oval"),
                    ("arch", "Arch"),
                    ("petal", "Petal"),
                    ("bloom", "Bloom"),
                    ("leaf", "Leaf"),
                    ("scallop", "Scallop"),
                    ("blob", "Blob"),
                    ("hexagon", "Hexagon"),
                ],
                default="bloom",
                help_text="Shape of the image frame. Only used when an image is present.",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="expertisearea",
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