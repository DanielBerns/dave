# your_project_name/app/tools.py
from datetime import datetime
from random import choices, randrange
from typing import Tuple


def generate_random_label(string_length: int = 32) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=string_length))


def base_256(number: int) -> Tuple[int, int, int]:
    """
    Converts a non-negative integer to a base-256 representation.

    Args:
        number: The integer to convert (must be between 0 and 16777215 inclusive).

    Returns:
        A tuple of three integers representing the base-256 identifiers
        (most significant to least significant).

    Raises:
        AssertionError: If the input number is out of range.
    """
    assert 0 <= number < 16777216, f"Input number must be between 0 and 16777215. Got {number}"
    third_identifier = number % 256
    number >>= 8  # Equivalent to number //= 256
    second_identifier = number % 256
    first_identifier = number >> 8  # Equivalent to number //= 256
    return first_identifier, second_identifier, third_identifier


def base_10(first_identifier: int, second_identifier: int, third_identifier: int) -> int:
    """
    Converts a three-identifier base-256 number to its base-10 representation.

    Args:
        first_identifier: The most significant identifier (0-255).
        second_identifier: The middle identifier (0-255).
        third_identifier: The least significant identifier (0-255).

    Returns:
        The integer representation of the base-256 number.
    """
    return (((first_identifier << 8) + second_identifier) << 8) + third_identifier


def get_identifiers_from_number(number: int) -> Tuple[str, str, str]:
    """
    Generates three zero-padded string identifiers with three decimal digits from an integer.

    Args:
        number: The integer to convert (must be between 0 and 16777215 inclusive).

    Returns:
        Three 3-character strings (e.g., "000", "001", "020").
    """
    first_identifier, second_identifier, third_identifier = base_256(number)
    return (f"{first_identifier:03d}", f"{second_identifier:03d}", f"{third_identifier:03d}")


