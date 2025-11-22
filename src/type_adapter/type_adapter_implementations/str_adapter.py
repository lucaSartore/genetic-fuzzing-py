from type_adapter.type_adapter import AdaptedType, TypeAdapter
from typing import Self

# ALLOWED_CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz _-1234567890"
ALLOWED_CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# ALLOWED_CHARACTERS = "IVXCML"

class StrAdapter(TypeAdapter[str]):

    def __init__(self, value: str) -> None:
        self._value = value

    @classmethod
    def initialize(cls, random, adapted_type: AdaptedType = None, initial_value: str | None = None) -> Self:
        """
        Initializes the individual. If no value is provided, generates a random string
        of random length (between 1 and 10 characters) to start the population.
        """
        if initial_value is not None:
            return cls(initial_value)
        
        # Generate a random length between 1 and 10 for initialization
        length = random.randint(1, 5)
        random_string = "".join(random.choice(ALLOWED_CHARACTERS) for _ in range(length))
        return cls(random_string)

    def get_value(self) -> str:
        return self._value

    @classmethod
    def crossover(cls, random, a: StrAdapter, b: StrAdapter) -> StrAdapter: #type: ignore
        """
        Performs single-point crossover.
        We take a slice from Parent A and a slice from Parent B.
        """
        val_a = a.get_value()
        val_b = b.get_value()

        # Handle edge cases with empty strings
        len_a = len(val_a)
        len_b = len(val_b)
        
        if len_a == 0: return cls(val_b)
        if len_b == 0: return cls(val_a)

        # Single Point Crossover
        # We pick a cut point relative to the smaller string to ensure overlap,
        # but crossover can result in variable lengths.
        min_len = min(len_a, len_b)
        cut_point = random.randint(0, min_len)

        # Child takes head of A and tail of B
        new_val = val_a[:cut_point] + val_b[cut_point:]
        
        return cls(new_val)

    def mutate(self, random) -> None:
        """
        Performs one of three mutations to allow exploring both content and length:
        1. Substitution: Change a character.
        2. Insertion: Add a character (Length +).
        3. Deletion: Remove a character (Length -).
        """
        current_val = self._value
        n = len(current_val)

        # Weighted choice for mutation type
        # 0: Substitution (50%), 1: Insertion (25%), 2: Deletion (25%)
        mutation_type = random.choices([0, 1, 2], weights=[50, 25, 25], k=1)[0]

        if mutation_type == 0 and n > 0:
            # Substitution
            pos = random.randint(0, n - 1)
            new_char = random.choice(ALLOWED_CHARACTERS)
            # Reconstruct string with new char
            self._value = current_val[:pos] + new_char + current_val[pos+1:]

        elif mutation_type == 1:
            # Insertion
            pos = random.randint(0, n) # Can insert at end
            new_char = random.choice(ALLOWED_CHARACTERS)
            self._value = current_val[:pos] + new_char + current_val[pos:]

        elif mutation_type == 2 and n > 0:
            # Deletion
            pos = random.randint(0, n - 1)
            self._value = current_val[:pos] + current_val[pos+1:]
        
        # If mutation resulted in empty string, potentially re-seed to avoid extinction of genetic material
        if len(self._value) == 0:
            self._value = random.choice(ALLOWED_CHARACTERS)

    def deep_copy(self) -> StrAdapter:
        # Strings are immutable, so we just pass the value to a new instance
        return StrAdapter(self._value)

    @classmethod
    def get_type(cls) -> type[str]:
        return str
