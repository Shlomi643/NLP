import re
from bs4 import BeautifulSoup as bs
from Utilities import Utils


class Formatter:
    # Fields:
    movie_name = None
    soup = None
    script_map = None

    # Static:
    name_format = "^(.)*::"
    person_spc = '___'
    garbage_spc = '~~~'
    text_spc = ';;;'
    song_spc = '~~~'
    cont = " (CONT'D)"

    def __init__(self, name):
        self.movie_name = name
        self.soup = bs(Utils.script(name), features='html.parser')
        self.script_map = Formatter.get_script_map(self.soup)

    @staticmethod
    def is_person(line):
        return line.startswith(Formatter.person_spc)

    @staticmethod
    def is_text(line):
        return line.startswith(Formatter.text_spc)

    @staticmethod
    def get_person(line):
        matcher = re.match(Formatter.name_format, line)
        return None if matcher is None or line.startswith('(') else matcher.group(0)[:-2]

    @staticmethod
    def get_text(line):
        return re.split(Formatter.name_format, line).pop().lstrip().lower()

    @staticmethod
    def get_script_list(lst):
        ret = []
        for line in lst:
            ret.append({'person': Formatter.get_person(line).rstrip(' '), 'text': Formatter.get_text(line)})
        return ret

    @staticmethod
    def get_script_map(soup):
        text = soup.findAll('p')
        ret = []
        for td in text:
            line = td.string
            if Formatter.is_person(line):
                line = (line[3:line.index('(')] if '(' in line else line[3:]) + ':: '
                if Formatter.get_person(line) is None:
                    print(line)
                    continue
            elif Formatter.is_text(line):
                curr = ret.pop()
                line = curr + line[3:] + ' '
            else:
                continue
            line = re.sub("\\(.*\\)", "", line)
            ret.append(line)
        return Formatter.get_script_list(ret)

    def get_char_tokens(self, person):
        ret = []
        for col in self.script_map:
            if col['person'].upper() == person.upper():
                ret += Utils.get_token(col['text'])
        return ret

    def get_tokens(self):
        ret = []
        for col in self.script_map:
            ret += Utils.get_token(col['text'])  # col['text'].lower().split()
        return ret

    def get_characters(self):
        ret = []
        for col in self.script_map:
            ret.append(col['person'])
        return list(dict.fromkeys(ret))  # remove redundancies

    def get_chars_tuples(self):
        x = self.get_words_num()
        x = sorted(x.items(), key=lambda y: y[1])
        x.reverse()
        return x  # list(map(lambda tup: tup[0], x))

    def get_words_num(self):
        my_map = self.script_map
        ret = {}
        for col in my_map:
            x = col['person']
            count = len(Utils.get_token(col['text']))
            ret[x] = count if x not in ret.keys() else ret[x] + count
        return ret
