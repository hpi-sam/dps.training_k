from django.db.models import CheckConstraint, Q, Value
from django.db.models.functions import Coalesce


def one_or_more_field_not_null(fields, suffix):

    checks = [Q(**{f"{field}__isnull": False}) for field in fields]

    check_condition = checks.pop()
    for check in checks:
        check_condition |= check

    return CheckConstraint(
        check=check_condition,
        name=f"one_or_more_field_not_null_{suffix}",
    )
