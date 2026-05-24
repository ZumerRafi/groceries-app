from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Expense(models.Model):

    CATEGORY_CHOICES = [

        ('Groceries', 'Groceries'),
        ('Snacks', 'Snacks'),
        ('Cleaning', 'Cleaning'),
        ('Transport', 'Transport'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Groceries'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    description = models.CharField(
        max_length=255
    )

    image = models.ImageField(
        upload_to='receipts/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_expired(self):

        return timezone.now() > (
            self.created_at + timedelta(days=30)
        )

    def __str__(self):

        return f"{self.user.username} - £{self.amount}"