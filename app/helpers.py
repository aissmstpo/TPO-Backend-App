def expect(input, expectedType, field):
    if isinstance(input, expectedType):
        return input
    else:
        raise AssertionError(f"No {field}!")
