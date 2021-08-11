import re


def search(regex: str, string: str):
    """
    find the sub-strings that match the pattern;
    :param regex: a regex pattern;
    :param string: string
    :return: a match_dict or a match_list;
    """
    match_dict = dict()
    iterator = re.finditer(regex, string)

    return iterator