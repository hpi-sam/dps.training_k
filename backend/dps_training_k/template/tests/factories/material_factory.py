import factory
from uuid import UUID
from template.models.material import Material


class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material
        django_get_or_create = ("name", "uuid", "is_reusable", "category")

    name = "Material"
    uuid = UUID("49df190b-06b8-4439-b055-86235b2c5779")
    is_reusable = "Material"
    category = Material.Category.DEVICE
