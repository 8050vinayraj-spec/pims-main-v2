from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AccountApproval

@receiver(post_save, sender=AccountApproval)
def sync_user_approval(sender, instance, **kwargs):
    """
    Sync AccountApproval status with CustomUser.is_approved.
    Ensures that whenever an officer approves/rejects a user,
    the CustomUser flag is updated immediately.
    """
    approved = (instance.status == 'APPROVED')
    user = instance.user

    if user.is_approved != approved:
        user.is_approved = approved
        user.save(update_fields=['is_approved'])