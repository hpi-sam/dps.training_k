import factory

from template.models.material import Material


class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material
        django_get_or_create = ("name", "uuid", "reusable", "category")

    name = "Material"
    uuid = "49df190b-06b8-4439-b055-86235b2c5779"
    reusable = True
    category = Material.Category.DEVICE
