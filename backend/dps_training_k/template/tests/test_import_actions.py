from django.test import TestCase
from unittest.mock import patch
from template.management.commands.import_actions import (
    Command as ImportActionsCommand,
)


class TestPopulateActionsCommand(TestCase):
    def test_defaults_structure(self):
        with patch(
            "template.models.Action.objects.update_or_create"
        ) as mocked_update_or_create:
            # execute import_actions command
            cmd = ImportActionsCommand()
            cmd.handle()

            # iterate over all calls made to "Action.objects.update_or_create"
            for call_args in mocked_update_or_create.call_args_list:
                _, kwargs = call_args
                name = kwargs.get("name", {})
                defaults = kwargs.get("defaults", {})
                self.assertIsInstance(
                    defaults["category"],
                    str,
                    f"{defaults['category']} is not a string",
                )
                self.assertTrue(
                    isinstance(defaults["application_duration"], type(None))
                    or isinstance(defaults["application_duration"], int),
                    f"{defaults['application_duration']} is neither an int nor a NoneType",
                )
                self.assertTrue(
                    isinstance(defaults["effect_duration"], type(None))
                    or isinstance(defaults["effect_duration"], int),
                    f"{defaults['effect_duration']} is neither an int nor a NoneType",
                )
                conditions = defaults["conditions"]
                self.assertTrue(
                    isinstance(conditions["required_actions"], type(None))
                    or isinstance(conditions["required_actions"], list),
                    f"{conditions['required_actions']} is neither a list nor a NoneType",
                )
                self.assertTrue(
                    isinstance(conditions["prohibitive_actions"], type(None))
                    or isinstance(conditions["prohibitive_actions"], list),
                    f"{conditions['prohibitive_actions']} is neither a list nor a NoneType",
                )
                self.assertTrue(
                    isinstance(conditions["material"], type(None))
                    or isinstance(conditions["material"], list),
                    f"{conditions['material']} is neither a list nor a NoneType",
                )
                self.assertTrue(
                    isinstance(conditions["num_personnel"], int),
                    f"{conditions['num_personnel']} is not an int",
                )
                self.assertTrue(
                    isinstance(conditions["lab_devices"], type(None))
                    or isinstance(conditions["lab_devices"], list),
                    f"{conditions['lab_devices']} is neither a list nor a NoneType",
                )
                self.assertTrue(
                    isinstance(conditions["area"], type(None))
                    or isinstance(conditions["area"], str),
                    f"{conditions['area']} is neither a string nor a NoneType",
                )
                self.assertTrue(
                    isinstance(conditions["role"], list),
                    f"{conditions['role']} is not a list ",
                )
                num_personnel = 0
                for entry in conditions["role"]:
                    if isinstance(entry, dict):
                        # Check each dict in 'role' has exactly one key-value pair
                        self.assertEqual(
                            len(entry),
                            1,
                            f"the role entry {entry} has more than 1 key value pair",
                        )

                        key = next(iter(entry))
                        value = entry[key]
                        self.assertIsInstance(key, str)
                        self.assertIsInstance(value, int)
                        num_personnel += value
                    elif isinstance(entry, list):
                        # Handle list entries, which represent alternative personnel roles
                        for e in entry:
                            self.assertEqual(
                                len(e),
                                1,
                                f"the role entry {e} has more than 1 key value pair",
                            )

                            key = next(iter(e))
                            value = e[key]
                            self.assertIsInstance(key, str)
                            self.assertIsInstance(value, int)
                        num_personnel += value  # only add once cause a list means "or"
                    else:
                        raise Exception("role may only contain lists and dicts")
                
                self.assertEqual(
                    conditions["num_personnel"],
                    num_personnel,
                    f"number of personnel doesn't match for {name}",
                )
