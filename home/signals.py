# Usar o signals para criar tudo na hora, tipo o carrinho, etc

import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from home.models import Products

# SENDER: <class 'home.models.Products'>
# INSTANCE: NOME DO PRODUTO
# USING: default
# ORIGIN: NOME DO PRODUTO
# KWARGS: {'signal': <django.db.models.signals.ModelSignal object at 0x0000013BF4640E00>} # noqa E501


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        pass


@receiver(pre_delete, sender=Products)
def remove_cover(sender, instance, using, origin, **kwargs):
    delete_cover(instance)


@receiver(pre_save, sender=Products)
def remove_cover_if_is_updated(sender, instance, **kwargs):
    if instance.id:
        old_model = Products.objects.filter(pk=instance.pk).first()

        if old_model.cover != instance.cover:
            delete_cover(old_model)
