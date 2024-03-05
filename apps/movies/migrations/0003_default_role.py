from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_third_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personfilmwork",
            name="role",
            field=models.CharField(
                choices=[("director", "Director"), ("writer", "Writer"), ("actor", "Actor")],
                default="actor",
                verbose_name="Role",
            ),
        ),
    ]
