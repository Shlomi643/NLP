import re

name_format = "^([A-Z]|[a-z]|\\s|\\.|[0-9])*:"


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
            # print(line)
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
            ret += get_token(col['text'])
    return ret


def get_tokens(soup):
    my_map = get_script_map(soup)
    ret = []
    for col in my_map:
        ret += get_token(col['text'])  # col['text'].lower().split()
    return ret


def get_token(line):
    def rpl(y): return line.replace(y, ' ')
    for x in [',', '.', ';', '?', '!', '/']:
        line = rpl(x)
    return line.split()


def get_characters(soup):
    my_map = get_script_map(soup)
    ret = []
    for col in my_map:
        ret.append(col['person'])
    return list(dict.fromkeys(ret))  # remove redundancies
