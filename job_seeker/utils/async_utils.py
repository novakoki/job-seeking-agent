async def async_enumerate(async_iterable, start=0):
    """Asynchronously enumerate an async iterator from a given start value"""
    n = start
    async for elem in async_iterable:
        yield n, elem
        n += 1
