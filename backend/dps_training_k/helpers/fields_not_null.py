from django.db.models import CheckConstraint, Q


def one_or_more_field_not_null(fields, suffix):
    """:params suffix: used to make the constraint name unique - e.g. the model name could be used."""
    checks = [Q(**{f"{field}__isnull": False}) for field in fields]

    check_condition = checks.pop()
    for check in checks:
        check_condition |= check

    return CheckConstraint(
        check=check_condition,
        name=f"one_or_more_field_not_null_{suffix}",
    )


def exactly_one_field_not_null(fields, suffix):
    """:params suffix: used to make the constraint name unique - e.g., the model name could be used."""
    # Create a list of Q objects where each checks if one field is non-null and others are null
    checks = []
    for i in range(len(fields)):
        non_null_field = fields[i]
        null_fields = fields[:i] + fields[i + 1 :]
        # Create Q object for current non-null field
        current_check = Q(**{f"{non_null_field}__isnull": False})
        # Add conditions for all other fields to be null
        for field in null_fields:
            current_check &= Q(**{f"{field}__isnull": True})
        checks.append(current_check)

    # Combine all checks using OR, since exactly one should be True
    check_condition = checks.pop()
    for check in checks:
        check_condition |= check

    return CheckConstraint(
        check=check_condition, name=f"exactly_one_field_not_null_{suffix}"
    )
