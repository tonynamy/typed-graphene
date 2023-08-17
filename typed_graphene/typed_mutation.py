from __future__ import annotations

from typing import Any, TypedDict

from graphene import Mutation

from .utils import python_type_to_graphene_instance


class TypedMutation(Mutation):
    """
    Wraps graphene.Mutation to support type-hinted arguments

    .. code:: python
        from typing import Any, Self, Unpack

        from typed_graphene import TypedMutation, TypedField

        class CreatePerson(TypedMutation):
            class TypedArguments(TypedMutation.TypedArguments):
                name: str

            ok = TypedField(bool)
            person = TypedField(Person)

            @classmethod
            def mutate(parent: Any, info: Any, **data: Unpack[TypedArguments]) -> Self:
                name = data["name"] # type: str

                person = Person(name=name)
                ok = True
                return CreatePerson(person=person, ok=ok)

        class Mutation(ObjectType):
            create_person = CreatePerson.Field(required=True)
    """

    class TypedArguments(TypedDict):
        pass

    @classmethod
    def __init_subclass_with_meta__(cls, *args: Any, **kwargs: Any) -> None:
        class GrapheneArguments:
            pass

        for name, T in cls.TypedArguments.__annotations__.items():
            setattr(GrapheneArguments, name, python_type_to_graphene_instance(T))

        cls.Arguments = GrapheneArguments

        return super(TypedMutation, cls).__init_subclass_with_meta__(*args, **kwargs)

    class Meta:
        abstract = True
