from django.db import migrations, models
import uuid

def create_uuid(apps, schema_editor):
    Institution = apps.get_model('clients', 'Userprofile')
    for inst in Institution.objects.all():
        inst.qrcode_id = uuid.uuid4()
        inst.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_userprofile_rating_num_userprofile_rating_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='qrcode_id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
        migrations.RunPython(create_uuid),

        migrations.AlterField(
            model_name='userprofile',
            name='qrcode_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True)
        )

    ]
