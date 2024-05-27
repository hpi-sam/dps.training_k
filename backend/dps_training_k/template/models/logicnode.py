from django.db import models

class LogicNode(models.Model):
    class Meta:
        ordering = ["state_transition"]

    class NodeType(models.TextChoices):
        NOT = "N", "not"
        AND = "A", "and"
        SUBCONDITION = "S", "subcondition"
        TRUE = "T", "true"

    state_transition = models.ForeignKey(
        "StateTransition", related_name="logic_nodes", on_delete=models.CASCADE, null=True, blank=True
    )
    node_type = models.CharField(choices=NodeType.choices, default=NodeType.TRUE, max_length=1)
    subcondition = models.ForeignKey(
        "Subcondition", related_name="logic_nodes", on_delete=models.SET_NULL, null=True, blank=True
    )
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        # has db fetches, maybe this shouldn't -> admin page will take long time to load because
        # of linear amount of db queries. Might put this logic in __repr__ instead
        name = f"Node #{self.id} "
        is_leaf = self.children.exists()
        if self.is_root():
            name += "(Root)"
        if is_leaf:
            name += "(Leaf) "
        name += self.get_node_type_display()
        if not is_leaf:
            name += " on "
            for node in self.children.all():
                name += f"#{node.id}, "
        if self.subcondition is not None:
            name += " " + self.subcondition.name
        if self.state_transition:
            name += f" of Condition # {self.condition_id}"
        return name

    def is_root(self):
        return self.parent is None

    def evaluate_tree(self, subconditions_dict):
        """
        Evaluates the evaluation tree starting with self
        :param subconditions_dict: A Dictionary of all Sub-Conditions that shows if they are fulfilled
        :return: Boolean
        """
        children_values = [
            child.evaluate_tree(subconditions_dict)
            for child in self.children.select_related("subcondition").all()
        ]
        if self.node_type == LogicNode.NodeType.TRUE:
            return True
        if self.node_type == LogicNode.NodeType.NOT:
            if len(children_values) != 1:
                raise Exception(
                    "NOT logical gate only allows one child, now there are "
                    + str(len(children_values))
                    + " children"
                )
            return not children_values[0]
        if self.node_type == LogicNode.NodeType.AND:
            if len(children_values) < 2:
                raise Exception(
                    "AND logical gate needs at least two children!"
                )
            return all(children_values)
        if self.node_type == LogicNode.NodeType.SUBCONDITION:
            return subconditions_dict[self.subcondition.id]
