import uuid
from typing import ClassVar

from django.contrib.postgres.functions import TransactionNow
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created = models.DateTimeField(
        db_default=TransactionNow(),
        editable=False,
    )

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        db_default=TransactionNow(),
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        is_update = not self._state.adding and not kwargs.get("force_insert", False)

        if is_update:
            update_fields = kwargs.get("update_fields")

            if update_fields is not None:
                if not update_fields:
                    return super().save(*args, **kwargs)

                kwargs["update_fields"] = {*update_fields, "modified"}

            self.modified = TransactionNow()

        super().save(*args, **kwargs)

        if is_update:
            self.refresh_from_db(fields=("modified",))

        return None


class FilmTypes(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv show", _("tv show")


class Roles(models.TextChoices):
    ACTOR = "actor", _("actor")
    DIRECTOR = "director", _("director")
    WRITER = "writer", _("writer")


class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.CharField(
        _("genre"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = '"content"."genre"'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Person(UUIDMixin, CreatedMixin, ModifiedMixin):
    full_name = models.CharField(
        _("name"),
        max_length=255,
    )

    class Meta:
        managed = False
        db_table = '"content"."person"'
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_("title"))
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation date"), blank=True, null=True)
    rating = models.FloatField(_("rating"), blank=True, null=True)
    type = models.CharField(
        _("type"),
        max_length=20,
        choices=FilmTypes.choices,
        default=FilmTypes.MOVIE,
    )
    certificate = models.CharField(
        _("certificate"),
        max_length=512,
        blank=True,
        null=True,
    )
    file_path = models.CharField(
        _("file path"),
        max_length=100,
        blank=True,
        null=True,
    )

    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmWork",
        verbose_name=_("genres"),
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmWork",
    )

    class Meta:
        managed = False
        db_table = '"content"."film_work"'
        verbose_name = _("film")
        verbose_name_plural = _("films")
        ordering = ("-creation_date",)

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin, CreatedMixin):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=_("genre"),
    )
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
    )

    class Meta:
        managed = False
        db_table = '"content"."genre_film_work"'
        verbose_name = _("genre")
        verbose_name_plural = _("film genres")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=("film_work", "genre"),
                name="gfw_film_genre_uniq",
                violation_error_message=_("Этот жанр уже добавлен к данному фильму."),
            ),
        ]

    def __str__(self):
        return self.genre.name


class PersonFilmWork(UUIDMixin, CreatedMixin):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name=_("person"),
    )
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        _("role"),
        max_length=50,
        choices=Roles.choices,
        default=Roles.ACTOR,
    )

    class Meta:
        managed = False
        db_table = '"content"."person_film_work"'
        verbose_name = _("person")
        verbose_name_plural = _("film persons")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=("film_work", "person", "role"),
                name="pfw_film_person_role_uniq",
                violation_error_message=_(
                    "Эта персона уже добавлена в данный фильм с указанной ролью."
                ),
            ),
        ]

    def __str__(self):
        return self.person.full_name
