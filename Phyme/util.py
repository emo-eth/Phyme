"""General utils"""
from typing import Iterable, TypeVar


T = TypeVar("T")


def flatten(x: Iterable[Iterable[T]]) -> Iterable[T]:
    """Generator of values from a 2d collection"""
    for y in x:
        yield from y
