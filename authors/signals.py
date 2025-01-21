from django.db.models.signals import post_save
from django.dispatch import receiver

from authors.models import User, UserProfile
from home.models import Cart


@receiver(post_save, sender=User)
def create_user_related_profiles(sender, instance, created, **kwargs):
    if created:
        try:
            cpf = instance.cpf

            if cpf:
                UserProfile.objects.create(user=instance.username, cpf=cpf)
            else:
                UserProfile.objects.create(user=instance.username)

        except AttributeError:
            pass

        Cart.objects.create(user=instance)
