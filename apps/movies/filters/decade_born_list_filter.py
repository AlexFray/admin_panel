from datetime import date

from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DecadeBornListFilter(admin.SimpleListFilter):
    title = _("Premier")

    parameter_name = "decade"

    def lookups(self, request, model_admin):
        return [
            ("80s", _("1980-1990")),
            ("90s", _("1990-2000")),
            ("00s", _("2000-2010")),
            ("10s", _("2010-2020")),
            ("new", _("2020+")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "80s":
            return queryset.filter(
                creation_date__gte=date(1980, 1, 1),
                creation_date__lte=date(1989, 12, 31),
            )
        if self.value() == "90s":
            return queryset.filter(
                creation_date__gte=date(1990, 1, 1),
                creation_date__lte=date(1999, 12, 31),
            )
        if self.value() == "00s":
            return queryset.filter(
                creation_date__gte=date(2000, 1, 1),
                creation_date__lte=date(2009, 12, 31),
            )
        if self.value() == "10s":
            return queryset.filter(
                creation_date__gte=date(2010, 1, 1),
                creation_date__lte=date(2019, 12, 31),
            )
        if self.value() == "new":
            return queryset.filter(
                creation_date__gte=date(2010, 1, 1),
                creation_date__lte=date(2030, 12, 31),
            )
