from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0016_task_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedtask',
            name='duration',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
