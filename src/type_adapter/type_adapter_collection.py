from type_adapter.type_adapter import TypeAdapter
from typing import Any, Dict


class TypeAdapterCollection:

    COLLECTION: None | TypeAdapterCollection = None

    @staticmethod
    def get_singleton() -> TypeAdapterCollection:
        if TypeAdapterCollection.COLLECTION is None:
            TypeAdapterCollection.COLLECTION = TypeAdapterCollection()
        return TypeAdapterCollection.COLLECTION

    def __init__(self, use_default_adapters_list: bool = True) -> None:
        self.adapters: list[type[TypeAdapter[Any]]]
        # import here to avoid circular import
        from type_adapter.type_adapter_implementations.bool_adapter import BoolAdapter
        from type_adapter.type_adapter_implementations.int_adapter import IntAdapter
        from type_adapter.type_adapter_implementations.float_adapters import FloatAdapter
        from type_adapter.type_adapter_implementations.list_adapter import ListAdapter
        from type_adapter.type_adapter_implementations.str_adapter import StrAdapter
        

        if use_default_adapters_list:
            self.adapters = [
                ListAdapter,
                IntAdapter,
                FloatAdapter,
                BoolAdapter,
                StrAdapter
            ]
        else:
            self.adapters = []

        self.adapters_dict = self.init_adapter_dict()

    def add_adapters(self,  adapters: list[type[TypeAdapter[Any]]]):
        self.adapters += adapters
        self.adapters_dict = self.init_adapter_dict()

    @staticmethod
    def get_adapter_static[T](t: type[T]) -> type[TypeAdapter[T]]:
        instance = TypeAdapterCollection.get_singleton()
        return instance.get_adapter(t)

    def get_adapter[T](self, t: type[T]) -> type[TypeAdapter[T]]:
        try:
            value = self.adapters_dict[t]
            assert value.get_type() == t, 'adapter type mismatch'
            return value
        except KeyError:
            raise Exception(f"Unable to find a valid type adapter for type {t}\n"
                             "You may register a new adapter using the `add_adapters` method")

    def init_adapter_dict(self) -> Dict[type, type[TypeAdapter[Any]]]:
        to_return = {
            adapter.get_type(): adapter
            for adapter in self.adapters
        }

        if len(to_return) < len(self.adapters):
            print('WARNING: one or more adapters have being discarded as wehad')

        return to_return
