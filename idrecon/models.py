from django.db import models

class Contact(models.Model):
    class LinkPrecedence(models.TextChoices):
        PRIMARY = "primary", "Primary"
        SECONDARY = "secondary", "Secondary" # For localisation use _("Secondary")

    id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    linked_id = models.IntegerField(blank=True, null=True)
    link_precedence = models.CharField(max_length=1, choices=LinkPrecedence)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

