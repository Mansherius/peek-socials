import re
from dataclasses import dataclass
from typing import Optional


# =====================================================================
# Value Objects (Self-contained validation rules) -->  Set by frozen=True
# Values are immutable - Cannot be changed once set
# =====================================================================


"""
__post_init__ is a special function from the dataclass library that allows us to run checks
on the creation of the dataclass after running __init__
"""


@dataclass(frozen=True)
class UserId:
    """The immutable identity of a User.
    Representation (UUID, int, ULID) is left abstract for now.
    """
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("UserId cannot be empty.")


@dataclass(frozen=True)
class Username:
    """Unique display handle for a user.

    Invariants:
    - Required
    - Max 32 characters
    - Permitted chars: A-Z, a-z, 0-9, -, _
    - Case-insensitive equality
    """
    value: str

    # Allowed: alphanumeric, hyphens, underscores
    _VALID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

    def __post_init__(self):
        if not self.value:
            raise ValueError("Username is required.")

        if len(self.value) > 32:
            raise ValueError("Username cannot exceed 32 characters.")

        if not self._VALID_PATTERN.match(self.value):
            raise ValueError(f"Username '{self.value}' contains invalid characters.")

    @property
    def canonical(self) -> str:
        """Returns normalized string used for case-insensitive uniqueness checks."""
        return self.value.lower()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Username):
            return self.canonical == other.canonical
        return False


@dataclass(frozen=True)
class Email:
    """User email address. Required, but deliberately NOT unique to a User."""

    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Email is required.")
        # Full validation rules intentionally deferred for now.


@dataclass(frozen=True)
class ProfilePictureRef:
    """Optional reference to a profile picture stored in infrastructure (e.g., S3 key)."""
    reference: str


# =====================================================================
# Aggregate Root / Entity
# =====================================================================

class User:
    """User Entity.

    Identity is strictly defined by `id` (UserId).
    Two Users with different IDs are distinct entities, even if they share attributes.
    """

    def __init__(
            self,
            user_id: UserId,
            username: Username,
            email: Email,
            profile_picture: Optional[ProfilePictureRef] = None,
    ):
        self._id = user_id
        self.username = username
        self.email = email
        self.profile_picture = profile_picture

    @property
    def id(self) -> UserId:
        """Immutable identifier."""
        return self._id

    def __eq__(self, other: object) -> bool:
        """Entities are equal ONLY if their unique IDs match."""
        if isinstance(other, User):
            return self.id == other.id
        return False


# required to avoid runtime issues since the __eq__ operator overrides the default equivalence and also sets the entity
# to "unhashable"
    def __hash__(self) -> int:
        return hash(self.id)