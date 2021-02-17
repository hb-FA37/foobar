from solution import solution

test_cases = [
    ("vmxibkgrlm", "encryption"),
    ("wrw blf hvv ozhg mrtsg'h vkrhlwv?", "did you see last night's episode?"),
    ("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!","Yeah! I can't believe Lance lost his job at the colony!!"),
]

for case in test_cases:
    input_, expected = case
    result = solution(input_)

    print("{0} -> {1}; expected: {2}".format(
        input_, result, expected,
    ))
    assert result == expected

print("All tests passed succesfully!")
