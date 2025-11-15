import hashlib
from typing import Literal

# you can define other auxiliary functions

def calculate_checksum(
    data: bytes, 
    algorithm: Literal["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_224", "sha3_256", "sha3_384", "sha3_512", "strum", "blake2b", "blake2s"] = "sha256"
) -> str:
    """
    Calculates a hash (e.g., 'md5', 'sha256') for input data (bytes) using 'hashlib'.

    Args:
        data: The input data as bytes for which to calculate the hash.
        algorithm: The name of the hashing algorithm to use (e.g., 'md5', 'sha256', 'sha512').
                   Defaults to 'sha256'.
                   The Literal type hint provides common algorithms, but `hashlib.new()`
                   supports more and raises ValueError for unsupported ones.

    Returns:
        A string representing the hexadecimal digest of the calculated hash.

    Raises:
        ValueError: If the specified algorithm is not supported by the hashlib module.
    """
    try:
        # Create a new hash object for the specified algorithm
        hasher = hashlib.new(algorithm)
        # Update the hash object with the input data
        hasher.update(data)
        # Get the hexadecimal digest of the hash
        return hasher.hexdigest()
    except ValueError as e:
        raise ValueError(f"Unsupported hashing algorithm: '{algorithm}'. Details: {e}") from e


# add this ad the end of the file
EXPORT_FUNCTION = calculate_checksum
