import pytest

from security import BCryptPasswordHasher


def test_when_passwords_match():
    hasher = BCryptPasswordHasher()
    password = "Airforceproud96"
    hashed_password = hasher.hash(raw_password=password)
    assert hashed_password is not None
    assert len(hashed_password) > 0
    assert hashed_password != password
    assert hasher.verify(raw_password=password, hashed_password=hashed_password)


def test_when_passwords_does_not_match():
    hasher = BCryptPasswordHasher()
    password = "Airforceproud96"
    another_password = "spagetti"
    hashed_password = hasher.hash(raw_password=password)
    assert not hasher.verify(
        raw_password=another_password, hashed_password=hashed_password
    )
