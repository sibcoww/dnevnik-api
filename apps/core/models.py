from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model with created and updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel):
    """Base model with ID and timestamps."""
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True
