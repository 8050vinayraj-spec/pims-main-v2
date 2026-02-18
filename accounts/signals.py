from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AccountApproval

@receiver(post_save, sender=AccountApproval)
def sync_user_approval(sender, instance, **kwargs):
    approved = (instance.status == 'APPROVED')
    instance.user.is_approved = approved
    instance.user.save(update_fields=['is_approved'])
    print(f"🔥 Signal fired for {instance.user.username}: is_approved={approved}")