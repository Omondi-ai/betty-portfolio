import os
from pathlib import Path

import cloudinary.uploader
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = "Upload all local media files referenced by FileField/ImageField to Cloudinary."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be uploaded without actually uploading.",
        )
        parser.add_argument(
            "--delete-local",
            action="store_true",
            help="Delete the local file after a successful upload.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        delete_local = options["delete_local"]

        total_found = 0
        total_uploaded = 0
        total_skipped = 0
        total_failed = 0

        for model in apps.get_models():
            for field in model._meta.get_fields():
                if not isinstance(field, (models.FileField, models.ImageField)):
                    continue

                field_name = field.name
                qs = model.objects.exclude(**{f"{field_name}__isnull": True}).exclude(
                    **{field_name: ""}
                )

                for obj in qs.iterator():
                    file_field = getattr(obj, field_name)
                    if not file_field:
                        continue
                    name = file_field.name
                    if not name:
                        continue

                    local_path = Path(settings.MEDIA_ROOT) / name

                    # Skip files that are already Cloudinary URLs or remote URLs
                    if name.startswith(("http://", "https://", "res.cloudinary.com")):
                        total_skipped += 1
                        continue

                    if not local_path.exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f"[MISSING] {model.__name__}.{field_name} "
                                f"pk={obj.pk}: {local_path} does not exist"
                            )
                        )
                        total_skipped += 1
                        continue

                    total_found += 1
                    self.stdout.write(
                        f"[FOUND] {model.__name__}.{field_name} pk={obj.pk}: {local_path}"
                    )

                    if dry_run:
                        continue

                    try:
                        with open(local_path, "rb") as fh:
                            result = cloudinary.uploader.upload(
                                fh,
                                resource_type="auto",
                                folder="betty_portfolio",
                                use_filename=True,
                                unique_filename=True,
                            )
                        total_uploaded += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"[UPLOADED] {local_path} -> {result.get('secure_url')}"
                            )
                        )

                        if delete_local:
                            os.remove(local_path)
                            self.stdout.write(
                                self.style.WARNING(f"[DELETED LOCAL] {local_path}")
                            )

                    except Exception as exc:
                        total_failed += 1
                        self.stderr.write(
                            self.style.ERROR(
                                f"[FAILED] {local_path}: {exc}"
                            )
                        )

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Summary"))
        self.stdout.write(f"  Found:    {total_found}")
        self.stdout.write(f"  Uploaded: {total_uploaded}")
        self.stdout.write(f"  Skipped:  {total_skipped}")
        self.stdout.write(f"  Failed:   {total_failed}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("\nDry run only—nothing was uploaded.")
            )