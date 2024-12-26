def create_uuid(apps, schema_editor):
    Institution = apps.get_model('consortial_billing', 'Institution')
    for inst in Institution.objects.all():
        inst.referral_code = uuid.uuid4()
        inst.save()


class Migration(migrations.Migration):

    dependencies = [
        ('consortial_billing', '0031_supportlevel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='referral_code',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(create_uuid),
        migrations.AlterField(
            model_name='institution',
            name='referral_code',
            field=models.UUIDField(default=uuid.uuid4, unique=True)
        )
    ]
