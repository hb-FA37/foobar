from solution import solution

test_cases = [
    (3, [7, 3, 5, 1], [-1, 7, 6, 3]),
    (5, [19, 14, 28], [21, 15, 29]),
]


def add_max_example():
    from random import randint
    numbers = [randint(1, pow(2, 30) - 1) for _ in range(1, 10000)]
    # This will always fail since we expect an empty list, it's more of a test
    # of the input limit.
    test_cases.append(
        (30, numbers, [])
    )

# add_max_example()


for case in test_cases:
    h, q, expected = case
    result = solution(h, q)

    print("({0}, {1}) -> {2}; expected: {3}".format(
        h, q, result, expected,
    ))
    # value must be returned a string.
    assert result == expected

print("All tests passed succesfully!")
