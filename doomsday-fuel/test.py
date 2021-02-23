from solution import solution

test_cases = [
    # Trivial case; 1x1.
    (
        [
            [0],
        ],
        [1, 1],
    ),
    # Travial case; 2x2.
    (
        [
            [65, 11],
            [0, 0],
        ],
        [1, 1],
    ),
    # Example 1.
    (
        [
            [0, 1, 0, 0, 0, 1],
            [4, 0, 0, 3, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        [0, 3, 2, 9, 14],
    ),
    # Example 2.
    (
        [
            [0, 2, 1, 0, 0],
            [0, 0, 0, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        [7, 6, 8, 21],
    ),
    # Same as example1, but state 2 and 3 switched.
    (
        [
            [0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0],
            [4, 0, 0, 3, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        [0, 3, 2, 9, 14],
    ),
    # Same as 2, but state 2 all the way to the bottom.
    (
        [
            [0, 1, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 3, 4, 0],
        ],
        [7, 6, 8, 21],
    ),
]

for case in test_cases:
    m, expected = case
    result = solution(m)
    print("Result: {0} ; expected: {1}".format(result, expected))
    assert(result == expected)

print("All tests passed succesfully!")
