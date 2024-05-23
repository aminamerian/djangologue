from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Room Name"))
    created_by = models.ForeignKey(
        "auth.User",
        verbose_name=_("Creator"),
        on_delete=models.CASCADE,
        related_name="created_by_rooms",
    )
    members = models.ManyToManyField(
        "auth.User",
        verbose_name=_("Members"),
        through="Membership",
        related_name="member_rooms",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return self.name


class MembershipStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    CONFIRMED = "confirmed", _("Confirmed")
    REJECTED = "rejected", _("Rejected")


class Membership(models.Model):
    user = models.ForeignKey(
        "auth.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    room = models.ForeignKey(
        Room,
        verbose_name=_("Room"),
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    status = models.CharField(
        max_length=10,
        choices=MembershipStatus.choices,
        default=MembershipStatus.PENDING,
        verbose_name=_("Status"),
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Joined At"))

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class Message(models.Model):
    user = models.ForeignKey(
        "auth.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="messages",
    )
    room = models.ForeignKey(
        Room,
        verbose_name=_("Room"),
        on_delete=models.CASCADE,
        related_name="messages",
    )
    content = models.TextField(verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"\"{self.user.username}\" in \"{self.room.name}\" => {self.content}"
