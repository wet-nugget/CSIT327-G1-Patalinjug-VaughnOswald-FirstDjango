from django.db import migrations


def assign_admin_role_to_superusers(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    CustomUser.objects.using(schema_editor.connection.alias).filter(
        is_superuser=True
    ).update(role="ADMIN")


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_customuser_managers_alter_customuser_role"),
    ]

    operations = [
        migrations.RunPython(
            assign_admin_role_to_superusers,
            migrations.RunPython.noop,
        ),
    ]