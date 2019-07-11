# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
from treebeard.mp_tree import MP_Node


@python_2_unicode_compatible
class FlatReferral(models.Model):

    REFERRAL_STATUS_PENDING = 'P'
    REFERRAL_STATUS_REJECTED = 'R'
    REFERRAL_STATUS_CONFIRM = 'C'
    REFERRAL_STATUS_DEFAULT = REFERRAL_STATUS_PENDING
    REFERRAL_STATUS_CHOICES = (
        (REFERRAL_STATUS_PENDING, 'Pending'), 
        (REFERRAL_STATUS_REJECTED, 'Rejected'),
        (REFERRAL_STATUS_CONFIRM, 'Confirm') 
    )

    referrer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='referreds'
    )
    referred = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='referrers'
    )
    expires_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=2, choices=REFERRAL_STATUS_CHOICES, default=REFERRAL_STATUS_DEFAULT)

    class Meta:
        unique_together = (('referrer', 'referred'),)
        ordering = ['id']
        db_table = 'flat_referral'

    def __str__(self):
        return '{} => {}'.format(self.referrer, self.referred)

    def clean(self, *args, **kwargs):
        if self.referrer == self.referred:
            raise ValidationError(_('The referrer can not be referred.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(FlatReferral, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'referrals:flat_referral_detail',
            kwargs={'pk': self.pk}
        )


class Link(models.Model):

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE
    )

    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.token)


@python_2_unicode_compatible
class MultiLevelReferral(MP_Node):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE
    )

    node_order_by = ['user']
    path = models.CharField(max_length=25500)

    class Meta:
        db_table = 'multi_level_referral'

    def get_absolute_url(self):
        return reverse(
            'referrals:multi_level_referral_detail',
            kwargs={'pk': self.pk}
        )

    def __str__(self):
        return self.user.username
