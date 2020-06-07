import re


def get_regex_keys(pattern, wildcard=False):
    keys = []
    regex = r'\<\w+\>'
    if wildcard:
        regex = r'\{[a-z]+\}'
    matches = re.finditer(regex, pattern)
    while True:
        try:
            keys.append(matches.next().group()[1:-1])
        except StopIteration:
            break
    return keys
