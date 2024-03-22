class OneFieldNotNull:
    def clean(self):
        fields = [field.name for field in self.__class__._meta.get_fields()]
        fields_values = [getattr(self, field) for field in fields]
        fields_set = len(fields) - fields_values.count(None)
        default_fields = 1
        if fields_set < 1 + default_fields:
            raise Exception("Owner must have at least one field filled in.")
        if fields_set > 1 + default_fields:
            raise Exception("Owner can only have one field filled in.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
