from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0015_task_created_at_task_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Nízká'), ('medium', 'Střední'), ('high', 'Vysoká')], default='medium', max_length=10),
        ),
    ]
