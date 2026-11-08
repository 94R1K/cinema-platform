from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")
    search_fields = ("name",)
    readonly_fields = ("id", "created", "modified")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created", "modified")
    search_fields = ("full_name",)
    readonly_fields = ("id", "created", "modified")


class GenreFilmWorkInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        genre_ids = set()

        for form in self.forms:
            if form.errors or not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            genre = form.cleaned_data.get("genre")

            if genre is None:
                continue

            if genre.pk in genre_ids:
                raise ValidationError(
                    _("A genre can only be added once to a film.")
                )

            genre_ids.add(genre.pk)


class PersonFilmWorkInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        person_roles = set()

        for form in self.forms:
            if form.errors or not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            person = form.cleaned_data.get("person")
            role = form.cleaned_data.get("role")

            if person is None or role is None:
                continue

            key = (person.pk, role)

            if key in person_roles:
                raise ValidationError(
                    _("A person cannot have the same role twice in a film.")
                )

            person_roles.add(key)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    formset = GenreFilmWorkInlineFormSet
    autocomplete_fields = ("genre",)
    extra = 1


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    formset = PersonFilmWorkInlineFormSet
    autocomplete_fields = ("person",)
    extra = 1


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "get_genres",
    )
    list_filter = ("type", "genres")
    search_fields = ("title", "description", "=id")

    readonly_fields = ("id", "created", "modified")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "type",
                    "creation_date",
                    "rating",
                ),
            },
        ),
        (
            _("Additional information"),
            {
                "fields": (
                    "description",
                    "certificate",
                    "file_path",
                ),
            },
        ),
        (
            _("System information"),
            {
                "fields": (
                    "id",
                    "created",
                    "modified",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("genres")
        )

    @admin.display(description=_("genres"))
    def get_genres(self, obj):
        return ", ".join(genre.name for genre in obj.genres.all())
