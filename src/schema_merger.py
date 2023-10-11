from deepmerge import Merger, always_merger
from abc import ABC, abstractmethod, ABCMeta


class BaseSchemaMergeStrategy(ABC):

    @abstractmethod
    def merge(self, base_schema, extension_schema):
        pass


class ExtensionStrategy(BaseSchemaMergeStrategy):
    """
    Extension schema can add new properties but cannot override base schema.
    In case of a conflict, base schema declarations will be used.
    """

    def unique_append(config, path, base, nxt):
        """ a list strategy to append only unique elements. """
        if len(nxt) > 0:
            if isinstance(nxt[0], str):
                base.extend(x for x in nxt if x not in base)
            else:
                base.extend(nxt)
        return base

    my_merger = Merger(
        [
            (list, [unique_append, "append"]),
            (dict, ["merge"]),
            (set, ["union"])
        ],
        ["use_existing"],
        ["use_existing"]
    )

    def merge(self, base_schema, extension_schema):
        return self.my_merger.merge(base_schema, extension_schema)


class OverrideStrategy(BaseSchemaMergeStrategy):
    """
    Extension schema can both add new properties and override base schema properties.
    In case of a conflict, extension schema declarations will override the base schema.
    """

    def merge(self, base_schema, extension_schema):
        return always_merger.merge(base_schema, extension_schema)
