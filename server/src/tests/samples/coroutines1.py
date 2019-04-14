# This same tests the type checker's ability to validate
# types related to coroutines (and async/await) statements.

from typing import Generator, Any
from asyncio import coroutine

async def coroutine1():
    return 1

a = coroutine1()

# This should generate an error because 'await'
# can't be used outside of an async function.
await a


def needs_int(val: int):
    pass

async def consumer1():
    # This should generate an error because
    # a is not an int
    needs_int(a)

    needs_int(await a)

    needs_int(await coroutine1())



class ScopedClass1:
    def __aenter__(self):
        return self

    @coroutine
    def __await__(self) -> Generator[Any, None, int]:
        yield 3
        return 3

async def consumer2():
    a = ScopedClass1()

    with a as b:
        # This should generate an error because
        # b is a Future, not an actual int.
        needs_int(b)

    async with a as b:
        needs_int(b)
