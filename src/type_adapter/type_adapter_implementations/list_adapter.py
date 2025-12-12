from types import GenericAlias
from typing import Self, List
from type_adapter.type_adapter import AdaptedType, TypeAdapter
# Assuming TypeAdapterCollection is available in your environment
from type_adapter.type_adapter_collection import TypeAdapterCollection 
import random 

class ListAdapter(TypeAdapter[list]):
    '''
    Type adapter for lists, implementing genetic operations that handle both 
    list length (sequence structure) and element content (using inner adapter).
    '''

    @classmethod
    def initialize(cls, random, adapted_type: AdaptedType, initial_value: list | None = None) -> Self:
        assert isinstance(adapted_type, GenericAlias) and adapted_type.__origin__ == list
        assert len(adapted_type.__args__) == 1
        
        inner_type = cls.parse_adapted_type(adapted_type.__args__[0])
        adapter_class = TypeAdapterCollection.get_adapter_static(
            cls.get_raw_time(inner_type)
        )
        
        value: list[TypeAdapter] = []
        
        if initial_value is not None:
            # Initialize from a provided list of raw values
            value = [
                adapter_class.initialize(random, inner_type, x) 
                for x in initial_value
            ]
        else:
            # Generate a random list of random length (1 to 5)
            length = random.randint(1, 5)
            value = [
                adapter_class.initialize(random, inner_type) 
                for _ in range(length)
            ]
            
        return cls(inner_type, value, adapter_class)
    
    # --- __init__ and get_value are kept from your baseline ---
    def __init__(self, inner_type: AdaptedType, value: list, adapter: type[TypeAdapter]) -> None:
        self.inner_type = inner_type
        self.value = value
        self.adapter = adapter

    def get_value(self) -> list:
        return [
            x.get_value()
            for x in self.value
        ]
    
    # -----------------------------------------------------------

    @classmethod
    def crossover(cls, random, a: Self, b: Self) -> Self: #type: ignore
        """
        Performs single-point crossover on the list of inner adapters.
        """
        val_a = a.value
        val_b = b.value

        len_a = len(val_a)
        len_b = len(val_b)
        
        if len_a == 0: return b.deep_copy()
        if len_b == 0: return a.deep_copy()

        min_len = min(len_a, len_b)
        cut_point = random.randint(0, min_len) 

        new_val = [x.deep_copy() for x in val_a[:cut_point]] + \
                  [x.deep_copy() for x in val_b[cut_point:]]
        
        return cls(a.inner_type, new_val, a.adapter)

    def mutate(self, random) -> None:
        """
        Performs one of three mutations on the list, mirroring the string strategy:
        1. Element Mutation (Substitution-equivalent): Mutate a single element's content.
        2. Insertion: Add a new element.
        3. Deletion: Remove an existing element.
        """
        current_list = self.value
        n = len(current_list)

        # Weighted choice for mutation type: 
        # 0: Element Mutation (50%), 1: Insertion (25%), 2: Deletion (25%)
        # Note: If n=0, we can only insert (type 1)
        
        mutation_choices = [0, 1]
        mutation_weights = [50, 25]
        
        if n > 0:
            mutation_choices.append(2)
            mutation_weights.append(25)
        
        # Normalize weights if necessary (random.choices does this automatically)
        mutation_type = random.choices(mutation_choices, weights=mutation_weights, k=1)[0]
        
        
        if mutation_type == 0 and n > 0:
            # Element Mutation (Content Change, equivalent to Substitution)
            # Choose a random element and mutate it using its own adapter
            pos = random.randint(0, n - 1)
            # The inner adapter object handles its own mutation
            self.value[pos].mutate(random)

        elif mutation_type == 1:
            # Insertion (Length +)
            # Choose a random position (including the end, pos=n)
            pos = random.randint(0, n) 
            # Initialize a brand new element using the inner adapter
            new_element = self.adapter.initialize(random, self.inner_type)
            self.value.insert(pos, new_element)

        elif mutation_type == 2 and n > 0:
            # Deletion (Length -)
            # Choose a random position to remove
            pos = random.randint(0, n - 1)
            self.value.pop(pos)
            
        # If mutation resulted in an empty list, re-seed with one element
        if len(self.value) == 0:
            self.value.append(self.adapter.initialize(random, self.inner_type))


    # --- deep_copy and get_type are kept from your baseline ---
    def deep_copy(self) -> Self:
        return self.__class__(
            self.inner_type,
            # Ensure we deep copy the *contents* of the list
            [x.deep_copy() for x in self.value],
            self.adapter
        )

    @classmethod
    def get_type(cls) -> type[list]:
        return list
