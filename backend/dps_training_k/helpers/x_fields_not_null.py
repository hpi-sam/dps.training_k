from django.db.models import CheckConstraint, Q, Value
from django.db.models.functions import Coalesce


def x_fields_not_null(amount_fields_not_null, fields):
    """
    Enforces that exactly `amount_fields_not_null` fields are not null.
    Works with SQL Coalesce function, for further info see: https://docs.djangoproject.com/en/1.8/ref/models/database-functions/#coalesce
    """
    checks = [
        Coalesce(Q(**{f"{field}__isnull": False}), Value(False)) for field in fields
    ]

    check_condition = checks.pop()
    for check in checks:
        check_condition += check

    return CheckConstraint(
        check=check_condition == amount_fields_not_null,
        name=f"exactly_{amount_fields_not_null}_fields_not_null",
    )
