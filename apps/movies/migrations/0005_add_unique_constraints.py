# Generated by Django 4.2.5 on 2024-02-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_add_indexes"),
    ]

    operations = [
#        migrations.AddConstraint(
#            model_name="filmwork",
#            constraint=models.UniqueConstraint(fields=("title",), name="unique_title"),
#        ),
#         migrations.AddConstraint(
#             model_name="genre",
#             constraint=models.UniqueConstraint(fields=("name",), name="unique_genre"),
#         ),
#         migrations.AddConstraint(
#             model_name="genrefilmwork",
#             constraint=models.UniqueConstraint(fields=("film_work", "genre"), name="unique_film_work_genre"),
#         ),
#         migrations.AddConstraint(
#             model_name="personfilmwork",
#             constraint=models.UniqueConstraint(fields=("film_work", "person"), name="unique_film_work_person"),
#         ),
    ]
