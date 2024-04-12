from enum import StrEnum
from enum import unique, auto

@unique
class Journal(StrEnum):
    """String Enum contaning all supported articles."""
    NATURE = auto()


