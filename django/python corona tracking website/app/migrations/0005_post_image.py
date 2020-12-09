

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_add_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
