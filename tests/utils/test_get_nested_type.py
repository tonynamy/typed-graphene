from typed_graphene.utils import get_nested_type
import pytest


def test_not_nested():  # type: ignore[no-untyped-def]
    T = str

    with pytest.raises(IndexError):
        get_nested_type(T)


def test_nested():  # type: ignore[no-untyped-def]
    T = list[str]

    expected_result = str
    result = get_nested_type(T)

    assert result == expected_result


def test_double_nested():  # type: ignore[no-untyped-def]
    T = list[list[str]]

    expected_result = list[str]
    result = get_nested_type(T)

    assert result == expected_result


def test_double_nested_complex():  # type: ignore[no-untyped-def]
    T = dict[int, list[str]]

    expected_result = int
    result = get_nested_type(T)

    assert result == expected_result
