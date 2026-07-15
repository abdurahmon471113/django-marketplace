from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = "active"
    ARCHIVED = "archived"
    WAITING = "waiting"
    REJECTED = "rejected"
