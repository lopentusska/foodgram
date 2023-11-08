from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager, models.Manager):
    """Custom user manager to create user and superuser."""
    def create_user(self, email, password=None, **kwargs):
        """Create and return a User with an email and password."""
        if email is None:
            raise TypeError('User must have an email.')
        if password is None:
            raise TypeError('User must have a password.')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        """Create and return a Superuser with an email and password."""
        if email is None:
            raise TypeError('Superuser must have an email.')
        if password is None:
            raise TypeError('Superuser must have a password.')

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with method
    to add/remove in favorites/shopping cart.
    """
    email = models.EmailField(db_index=True, max_length=254, unique=True)
    username = models.CharField(db_index=True, max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    favorite_recipes = models.ManyToManyField(
        'recipes_label.Recipe',
        related_name='favorited_by',
    )
    shopping_cart = models.ManyToManyField(
        'recipes_label.Recipe',
        related_name='in_shopping_cart',
    )

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def favorite(self, recipe):
        return self.favorite_recipes.add(recipe)

    def remove_favorite(self, recipe):
        return self.favorite_recipes.remove(recipe)

    def in_favorite(self, recipe):
        return self.favorite_recipes.filter(pk=recipe.pk).exists()

    def add_shopping_cart(self, recipe):
        return self.shopping_cart.add(recipe)

    def remove_shopping_cart(self, recipe):
        return self.shopping_cart.remove(recipe)

    def added_in_shopping_cart(self, recipe):
        return self.shopping_cart.filter(pk=recipe.pk).exists()
