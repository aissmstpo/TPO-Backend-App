def expect(input, expectedType, field):
    """
    Checks if the input field is of the expectedType

    :param input: argument to be checked
    :type input: object
    :param expectedType: expected type of the input argument
    :type expectedType: str
    :param field: name of the ``input`` field
    :type field: str
    :returns: ``input`` if the input field is of the expectedType
    :rtype: object
    :raises AssertionError: if the input field is not of the expectedType
    """
    if isinstance(input, expectedType):
        return input
    else:
        raise AssertionError(f"No {field}!")
