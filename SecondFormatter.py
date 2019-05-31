import re

name_format = "^([A-Z]|\\s|\\.|[0-9])*:"


def get_person(line):
    return re.match(name_format, line).group(0)[:-1]


def get_text(line):
    return re.split(name_format, line).pop().lstrip().lower()


def get_script_list(lst):
    ret = []
    for line in lst:
        ret.append({'person': get_person(line), 'text': get_text(line)})
    return ret


def get_script_map(soup):
    text = soup.findAll('td', {'class': 'line-content'})
    ret = []
    for td in text:
        line = td.string
        if not re.match(name_format, line):
            curr = ret.pop()
            line = curr + line
        line = re.sub("\\(.*\\)", "", line)
        ret.append(line)
    return get_script_list(ret)


def get_char_tokens(soup, person):
    my_map = get_script_map(soup)
    ret = []
    for col in my_map:
        if col['person'] == person.upper():
            ret += col['text'].split()
    return ret


def get_tokens(my_map):
    ret = []
    for col in my_map:
        ret += col['text'].lower().split()
    return ret
