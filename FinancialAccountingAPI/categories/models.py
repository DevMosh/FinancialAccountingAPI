from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CategoryUser(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username} - {', '.join(category.name for category in self.categories.all())}"

