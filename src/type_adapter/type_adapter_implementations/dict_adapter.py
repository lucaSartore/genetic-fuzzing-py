from type_adapter.type_adapter import AdaptedType, TypeAdapter
from types import GenericAlias
from typing import Any, Self, TypeVar, final

from type_adapter.type_adapter_collection import TypeAdapterCollection

class DictAdapter(TypeAdapter[dict]):

    @classmethod
    def initialize(cls, random, adapted_type: AdaptedType, initial_value: dict | None = None) -> Self:
        assert isinstance(adapted_type, GenericAlias) and adapted_type.__origin__ == dict
        assert len(adapted_type.__args__) == 2

        key_type = cls.parse_adapted_type(adapted_type.__args__[0])
        value_type = cls.parse_adapted_type(adapted_type.__args__[1])

        key_type_adapter = TypeAdapterCollection.get_adapter_static(
            cls.get_raw_time(key_type)
        )
        value_type_adapter = TypeAdapterCollection.get_adapter_static(
            cls.get_raw_time(value_type)
        )
        # since we can't put the type adapter as the key
        # (no hash implementation)
        # we put the raw value, and as the value we put a key-value tuple
        final_dict: dict[Any,tuple[TypeAdapter, TypeAdapter]] = {}

        if initial_value is not None:
            final_dict = {
                k: (
                    key_type_adapter.initialize(random, key_type, k),
                    value_type_adapter.initialize(random, value_type, v)
                )
                for k,v in initial_value.items()
            }
        else:
            length = random.randint(1, 5)
            for _ in range(length):
                k = key_type_adapter.initialize(random, key_type)
                v = value_type_adapter.initialize(random, value_type)
                final_dict[k.get_value()] = (k,v)

        return cls(final_dict, key_type, value_type)

    def __init__(self, final_dict: dict[Any, tuple[TypeAdapter, TypeAdapter]], key_type: AdaptedType, value_type: AdaptedType):
        self.final_dict = final_dict
        self.key_type = key_type
        self.value_type = value_type

    def get_value(self) -> dict:
        return {
            k.get_value(): v.get_value()
            for k,v in self.final_dict.values()
        }

    @classmethod
    def crossover(cls, random, a: DictAdapter, b: DictAdapter) -> DictAdapter: #type: ignore
        """
        Performs crossover by combining key-value pairs from Parent A and Parent B.
        - Keys present in both: we do a value-by-value crossover
        - Keys unique to A may be selected
        - Keys unique to B may be selected
        """
        
        # Get raw keys from both parents
        keys_a = set(a.final_dict.keys())
        keys_b = set(b.final_dict.keys())
        
        child_dict: dict[Any, tuple[TypeAdapter, TypeAdapter]] = {}

        # 1. Keys unique to A (kept entirely from A)
        unique_a = keys_a - keys_b
        for key in unique_a:
            if random.random() < 0.33:
                (k,v) = a.final_dict[key]
                child_dict[key] = (k.deep_copy(), v.deep_copy())
        
        # 2. Keys unique to B (kept entirely from B)
        unique_b = keys_b - keys_a
        for key in unique_b:
            if random.random() < 0.33:
                (k,v) = b.final_dict[key]
                child_dict[key] = (k.deep_copy(), v.deep_copy())
        
        # 3. Keys in common (conflict resolution)
        common_keys = keys_a.intersection(keys_b)
        
        for key in common_keys:
            (k,va) = a.final_dict[key]
            (_,vb) = b.final_dict[key]

            v = va.__class__.crossover(random, va, vb)
            child_dict[k] = (k.deep_copy(), v.deep_copy())

        return cls(child_dict, a.key_type, a.value_type)

    def mutate(self, random) -> None:
        """
        Performs one of four weighted mutations:
        1. Value Mutation: Mutate the value of an existing key (50%).
        2. Key Mutation: Mutate the key of an existing pair (15%).
        3. Insertion: Add a new key-value pair (20%).
        4. Deletion: Remove an existing key-value pair (15%).
        """
        
        current_keys = list(self.final_dict.keys())
        n = len(current_keys)

        # Mutation weights: 0:Value Mut(50), 1:Key Mut(15), 2:Insert(20), 3:Delete(15)
        # for an empty dict, only the insertion is an allowed mutation
        mutation_choices = [2]
        mutation_weights = [20]
        
        if n > 0:
            mutation_choices.extend([0,  1,  3])
            mutation_weights.extend([50, 15, 15])
        
        mutation_type = random.choices(mutation_choices, weights=mutation_weights, k=1)[0]

        if mutation_type == 0 and n > 0:
            ## 1. Value Mutation (Content Change, most common)
            old_raw_key = random.choice(current_keys)
            k_adapter, v_adapter = self.final_dict[old_raw_key]
            
            v_adapter.mutate(random)

            self.final_dict[old_raw_key] = (k_adapter, v_adapter)

        elif mutation_type == 1 and n > 0:
            ## 2. Key Mutation (Structure Change, less common)

            old_raw_key = random.choice(current_keys)
            k_adapter, v_adapter = self.final_dict.pop(old_raw_key)

            k_adapter.mutate(random)
            new_raw_key = k_adapter.get_value()

            # The value adapter is unchanged.
            self.final_dict[new_raw_key] = (k_adapter, v_adapter)
            
        elif mutation_type == 2:
            ## 3. Insertion (Size Change +)
            
            key_adapter_class = TypeAdapterCollection.get_adapter_static(self.get_raw_time(self.key_type))
            value_adapter_class = TypeAdapterCollection.get_adapter_static(self.get_raw_time(self.value_type))
            
            # Initialize new key adapter until a unique key is found
            k_adapter = key_adapter_class.initialize(random, self.key_type)
            k_raw = k_adapter.get_value()
            v_adapter = value_adapter_class.initialize(random, self.value_type)
            
            self.final_dict[k_raw] = (k_adapter, v_adapter)

        elif mutation_type == 3 and n > 0:
            ## 4. Deletion (Size Change -)
            raw_key_to_delete = random.choice(current_keys)
            self.final_dict.pop(raw_key_to_delete)
            

    def deep_copy(self) -> DictAdapter: #type: ignore
        return self.__class__(
            {
                k: (ka.deep_copy(), va.deep_copy())
                for k, (ka, va) in self.final_dict.items()
            },
            self.key_type,
            self.value_type
        )

    @classmethod
    def get_type(cls) -> type[dict]:
        return dict
