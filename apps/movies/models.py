import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        indexes = [
            models.Index(fields=["name"], name="genre_name_idx"),
        ]
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_genre")]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("Full Name"), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Actor")
        verbose_name_plural = _("Actors")
        indexes = [
            models.Index(fields=["full_name"], name="person_full_name_idx"),
        ]


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeChoices(models.TextChoices):
        MOVIE = "movie", _("Movie")
        TV_SHOW = "tv_show", _("TV show")

    title = models.CharField(_("Title"), blank=False, max_length=255, default=None)
    description = models.TextField(_("Description"), blank=True, null=True)
    creation_date = models.TextField(_("Premier"), blank=True, default="", null=True)
    file_path = models.CharField(_("File Path"), max_length=255, blank=True, null=True, default=None)
    rating = models.FloatField(_("Rating"), blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)], default=0.0, null=True)
    type = models.CharField(_("Type"), choices=TypeChoices.choices, default=TypeChoices.MOVIE, blank=False)
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
        indexes = [
            models.Index(fields=["creation_date"], name="film_work_creation_date_idx"),
            models.Index(fields=["rating"], name="film_work_rating_idx"),
            models.Index(fields=["title"], name="film_work_title_idx"),
            models.Index(fields=["rating", "creation_date"], name="film_work_rating_creation_idx"),
        ]
        constraints = [models.UniqueConstraint(fields=["title"], name="unique_title")]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        indexes = [
            models.Index(fields=["film_work", "genre"], name="film_work_genre_idx"),
        ]
        constraints = [models.UniqueConstraint(fields=["film_work", "genre"], name="unique_film_work_genre")]


class PersonFilmwork(UUIDMixin):
    class RoleChoices(models.TextChoices):
        DIRECTOR = "director", _("Director")
        WRITER = "writer", _("Writer")
        ACTOR = "actor", _("Actor")

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.CharField(_("Role"), choices=RoleChoices.choices, default=RoleChoices.ACTOR, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        indexes = [
            models.Index(fields=["film_work", "person"], name="film_work_person_idx"),
        ]
        constraints = [models.UniqueConstraint(fields=["film_work", "person"], name="unique_film_work_person")]
