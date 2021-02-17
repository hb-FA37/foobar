def solution(x):
    import string

    reversed_ascii = list(reversed(string.ascii_lowercase))
    converted = ""

    for letter in x:
        try:
            converted += reversed_ascii[string.ascii_lowercase.index(letter)]
        except ValueError:
            converted += letter

    return converted
