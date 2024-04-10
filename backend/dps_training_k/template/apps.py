from django.apps import AppConfig


class TemplateConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "template"

    # ToDo: Remove once database is populated by default
    """def ready(self):
        from template.models.action import Action

        Action.objects.get_or_create(
            name="Recovery Position",
            category=Action.Category.TREATMENT,
            duration=10,
            conditions=None,
        )"""
