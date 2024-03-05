from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db import models
from django.views.generic import DetailView
from django.views.generic.list import BaseListView
from django.utils.translation import gettext_lazy as _

from apps.movies.models import Filmwork, GenreFilmwork, PersonFilmwork


class MoviesApiMixin:
    model: models.Model
    http_method_names = ['get']

    def render_to_response(self, context, **response_kwargs):
        if not context:
            return JsonResponse(context, status=404)

        return JsonResponse(context)

    def get_queryset(self):
        return self.model.objects.prefetch_related('genres', 'persons')

    def get_film_works(self, queryset: models.Model) -> list[dict]:
        film_works = []

        for entry in queryset:
            film_work = {
                "id": entry.id,
                "title": entry.title,
                "description": entry.description,
                "creation_date": entry.creation_date,
                "rating": entry.rating,
                "type": entry.type,
            }

            film_work.update(entry.genres.aggregate(genres=ArrayAgg("name")))
            film_work.update(entry.persons.filter(personfilmwork__role="actor").aggregate(actors=ArrayAgg("full_name")))
            film_work.update(entry.persons.filter(personfilmwork__role="director").aggregate(directors=ArrayAgg("full_name")))
            film_work.update(entry.persons.filter(personfilmwork__role="writer").aggregate(writers=ArrayAgg("full_name")))

            film_works.append(film_work)

        return film_works


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        film_works = self.get_film_works(queryset)

        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": film_works,
        }


class MoviesDetailApi(MoviesApiMixin, DetailView):
    model = Filmwork

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset().filter(id=self.kwargs.get(self.pk_url_kwarg))

        try:
            [film_work] = self.get_film_works(queryset)
            return film_work
        except ValueError:
            print("Ничего не найдено")
            return None
