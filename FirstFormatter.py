import re

# name_format = "^([A-Z]|\\'|\\#|\\/|\\&|\\s|\\.|[0-9])*:"
name_format = "^(.)*::"
person_spc = '___'
garbage_spc = '~~~'
text_spc = ';;;'
song_spc = '~~~'
cont = " (CONT'D)"


def is_person(line):
    return line.startswith(person_spc)


def is_text(line):
    return line.startswith(text_spc)


def get_person(line):
    matcher = re.match(name_format, line)
    return None if matcher is None or line.startswith('(') else matcher.group(0)[:-2]


def get_text(line):
    return re.split(name_format, line).pop().lstrip().lower()


def get_script_list(lst):
    ret = []
    for line in lst:
        ret.append({'person': get_person(line).rstrip(' '), 'text': get_text(line)})
    return ret


def get_script_map(soup):
    text = soup.findAll('p')
    ret = []
    for td in text:
        line = td.string
        if is_person(line):
            line = (line[3:line.index('(')] if '(' in line else line[3:]) + ':: '
            if get_person(line) is None:
                print(line)
                continue
        elif is_text(line):
            curr = ret.pop()
            line = curr + line[3:] + ' '
        else:
            continue
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
        ret += (col['person'].replace(' & ', '/').split('/'))
    return list(dict.fromkeys(ret))  # remove redundancies
