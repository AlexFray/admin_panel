from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .filters.decade_born_list_filter import DecadeBornListFilter
from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name_plural = _("Genres")


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    verbose_name_plural = _("Actors")

    autocomplete_fields = ("person",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description", "id")

    list_per_page = 25


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = ("title", "type", "creation_date", "rating", "get_genres")
    list_filter = ("type", DecadeBornListFilter)
    search_fields = ("title", "description", "id")

    list_per_page = 25
    list_prefetch_related = ("genres",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(*self.list_prefetch_related)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _("Genres")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    search_fields = ("full_name", "id")

    list_per_page = 25
