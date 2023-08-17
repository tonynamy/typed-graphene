from typing import NotRequired, Optional, TypedDict, Union

from typed_graphene.utils import get_type_and_required


def test_union() -> None:
    T = Union[str, int]

    expected_result = Union[str, int], True
    result = get_type_and_required(T)  # type: ignore[arg-type]

    assert expected_result == result


def test_union_complex_none() -> None:
    T = Union[str, int, None]

    expected_result = Union[str, int], False
    result = get_type_and_required(T)  # type: ignore[arg-type]

    assert expected_result == result


def test_union_none() -> None:
    T = Union[str, None]

    expected_result = str, False
    result = get_type_and_required(T)  # type: ignore[arg-type]

    assert expected_result == result


def test_union_type() -> None:
    T = str | int

    expected_result = str | int, True
    result = get_type_and_required(T)  # type: ignore[arg-type]

    assert expected_result == result


def test_union_type_complex_none() -> None:
    T = str | int | None

    expected_result = str | int, False
    result = get_type_and_required(T)  # type: ignore[arg-type]

    assert expected_result == result


def test_union_type_none() -> None:
    T = str | None

    expected_result = str, False
    result = get_type_and_required(T)  # type: ignore[arg-type]

    assert expected_result == result


def test_not_required() -> None:
    class TestTypedDict(TypedDict):
        field: NotRequired[str]

    T = TestTypedDict.__annotations__["field"]

    expected_result = str, False
    result = get_type_and_required(T)

    assert expected_result == result


def test_optional() -> None:
    T = Optional[str]

    expected_result = str, False
    result = get_type_and_required(T)  # type: ignore[arg-type]

    assert expected_result == result


def test_required() -> None:
    T = str

    expected_result = str, True
    result = get_type_and_required(T)

    assert expected_result == result
