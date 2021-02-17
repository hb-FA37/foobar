from solution import solution

test_cases = [
    # Provided triangle.
    (1, 1, 1),
    (1, 2, 2),
    (1, 3, 4),
    (1, 4, 7),
    (2, 1, 3),
    (2, 2, 5),
    (2, 3, 8),
    (3, 1, 6),
    (3, 2, 9),
    (4, 1, 10),
    # Tests.
    (5, 10, 96),
    # TODO; figure out solution for this as it checks for recursion issues if
    # such a solution is used.
    # (100000, 100000, ??),
]

for case in test_cases:
    x, y, expected = case
    result = solution(x, y)

    print("({0}, {1}) -> {2}; expected: {3}".format(
        x, y, result, expected,
    ))
    # value must be returned a string.
    assert result == str(expected)

print("All tests passed succesfully!")
