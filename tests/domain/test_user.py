import pytest
from peek_socials.domain.user import Email, User, UserId, Username


# =====================================================================
# Value Object Invariant Tests
# =====================================================================

def test_username_rejects_invalid_characters():
    """
    ID: UNIT-DOMAIN-USER-01
    TYPE: Unit
    SUMMARY: Asserts Username("alice!") raises ValueError matching "invalid characters" due to forbidden exclamation mark.
    """
    with pytest.raises(ValueError, match="invalid characters"):
        Username("alice!")


def test_username_maintains_max_length():
    """
    ID: UNIT-DOMAIN-USER-02
    TYPE: Unit
    SUMMARY: Asserts Username with 33 characters raises ValueError matching "cannot exceed 32 characters".
    """
    with pytest.raises(ValueError, match="cannot exceed 32 characters"):
        Username("a" * 33)


def test_username_case_insensitive():
    """
    ID: UNIT-DOMAIN-USER-03
    TYPE: Unit
    SUMMARY: Asserts Username("Alice") == Username("aLiCe") evaluates to True via canonical lowercase comparison.
    """
    u1 = Username("Alice")
    u2 = Username("aLiCe")
    assert u1 == u2


def test_email_rejects_empty_string():
    """
    ID: UNIT-DOMAIN-USER-04
    TYPE: Unit
    SUMMARY: Asserts Email("   ") raises ValueError matching "Email is required" when initialized with whitespace.
    """
    with pytest.raises(ValueError, match="Email is required"):
        Email("   ")


# =====================================================================
# Entity Identity & State Tests
# =====================================================================

def test_user_creation_success_with_valid_attributes():
    """
    ID: UNIT-DOMAIN-USER-05
    TYPE: Unit
    SUMMARY: Asserts User initializes successfully with UserId("usr_100") and Username("alice"), matching its assigned properties.
    """
    user = User(
        user_id=UserId("usr_100"),
        username=Username("alice"),
        email=Email("alice@example.com")
    )
    assert user.id == UserId("usr_100")
    assert user.username == Username("alice")


def test_user_creation_fails_with_invalid_attributes():
    """
    ID: UNIT-DOMAIN-USER-06
    TYPE: Unit
    SUMMARY: Asserts passing Username("alice!") inside User instantiation propagates the "invalid characters" ValueError.
    """
    with pytest.raises(ValueError, match="invalid characters"):
        User(
            user_id=UserId("usr_100"),
            username=Username("alice!"),
            email=Email("alice@example.com")
        )


def test_user_equality_with_same_ids():
    """
    ID: UNIT-DOMAIN-USER-07
    TYPE: Unit
    SUMMARY: Asserts two User instances with matching UserId("1842") evaluate as equal despite differing username and email values.
    """
    user1 = User(
        user_id=UserId("1842"),
        username=Username("alice"),
        email=Email("alice@example.com")
    )
    user2 = User(
        user_id=UserId("1842"),
        username=Username("alice_renamed"),
        email=Email("new_email@example.com")
    )
    assert user1 == user2


def test_user_inequality():
    """
    ID: UNIT-DOMAIN-USER-08
    TYPE: Unit
    SUMMARY: Asserts two User instances with different IDs ("1001" vs "1002") evaluate as not equal despite identical username and email attributes.
    """
    user1 = User(
        user_id=UserId("1001"),
        username=Username("alice"),
        email=Email("alice@example.com")
    )
    user2 = User(
        user_id=UserId("1002"),
        username=Username("alice"),
        email=Email("alice@example.com")
    )
    assert user1 != user2