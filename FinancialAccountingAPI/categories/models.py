from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class CategoryUser(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'category'], name='unique_user_category')
        ]

