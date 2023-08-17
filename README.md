# typed-graphene

typed-graphene is a library that provides a type-safe interface for graphene-python.

## Examples

### Type-Safe Query

```python
from graphene import ObjectType, Field, String

class ExampleQuery(ObjectType):
	foo = Field(FooType, required=True, input_a=String(), input_b=String(required=True))

	def resolve_foo(self, info, **data) -> FooType:
		input_a = data.get("input_a") # any
		input_b = data["input_b"] # any
```

**graphene example**

```python
from typing import TypedDict, NotRequired

from graphene import Field
from typed_graphene import TypedField

class FooFieldArguments(TypedDict):
	input_a: NotRequired[str]
	input_b: str

class ExampleQuery(ObjectType):
	# `required=True` by default
	foo = TypedField(FooType, **FooFieldArguments.__annotations__)

	def resolve_foo(self, info, **data: Unpack[FooFieldArguments]) -> FooType:
		input_a = data.get("input_a") # str | None
		input_b = data["input_b"] # str
```

**typed-graphene exmaple**

### Type-Safe Mutation

```python
from graphene import Mutation, Field, String, Boolean

class Example(Mutation):
	class Arguments:
		input_a = String()
		input_b = String(required=True)

    ok = Field(Boolean, required=True)
	errors = Field(ExampleErrors)

	@classmethod
	def mutate(cls, root, info, **data) -> Self:
		input_a = data.get("input_a") # any
		input_b = data["input_b"] # any

	return cls(ok=True)
```

**graphene example**

```python
from dataclasses import dataclass
from typing import TypedDict, NotRequired

from typed_graphene import TypedBaseMutation, TypedField

class Example(TypedBaseMutation):
	class TypedArguments(TypedBaseMutation.TypedArguments):
		input_a: NotRequired[str]
		input_b: str

    ok = TypedField(bool)
	# concat type with ` | None` for `required=False`
	errors = TypedField(ExampleErrors | None)

	@classmethod
	def validate(cls, root, info, **data: Unpack[TypedArguments]) -> ExampleErrors:
		errors = ExampleErrors()

		errors.input_a = "error" # no error

		return errors

	@classmethod
	def execute(cls, root, info, **data: Unpack[TypedArguments]) -> Self:
		input_a = data.get("input_a") # str | None
		input_b = data["input_b"] # str

	return cls(ok=True)
```

**typed-graphene example**

## Topics

### Defining custom types

You can define custom types by inheriting from `BaseTransformer` and registering it with `register`.

```python
from graphene import ID
from typed_graphene import BaseTransformer, register

class IDStr(str):
    pass

@register
class IDStrTransformer(BaseTransformer):
    python_type = IDStr
    graphene_type = ID
```

You can also override `check_type` and `transform_type` to define custom type checking and transformation.
It is recommended to add `@cache` to the `check_type` and `transform_type` methods for performance and type-consistency.

```python
from typing import Literal, get_origin

from graphene import Literal
from typed_graphene import BaseTransformer, register

@register
class LiteralTransformer(BaseTransformer[Literal, Enum]):
    python_type = Literal
    graphene_type = Enum

    @classmethod
    @cache
    def check_type(cls, T):
        return get_origin(T) == Literal

    @classmethod
    @cache
    def transform_type(cls, T: type[Literal]) -> type[Enum]:
        """Transform the type into the graphene type."""
        return Enum.from_enum(literal_to_enum(T))

```

## Author

Jeong Yeon Nam(tonynamy@apperz.co.kr)
