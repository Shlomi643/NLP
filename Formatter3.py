import re
from bs4 import BeautifulSoup as bs
from Utilities import Utils


class Formatter:
    # Fields:
    movie_name = None
    soup = None
    script_map = None

    # Static:
    name_format = "^([A-Z]|[a-z]|\\,|\\-|\\#|\\'|\\&|\\s|\\.|[0-9])*:"

    def __init__(self, name):
        self.movie_name = name
        self.soup = bs(Utils.script(name), features='html.parser')
        self.script_map = Formatter.get_script_map(self.soup)

    @staticmethod
    def get_person(line):
        return re.match(Formatter.name_format, line).group(0)[:-1]

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
            if td.strong is not None:
                person = td.strong.string
                line = td.strong.next_sibling.replace('\n', ' ')
                ret.append(person + re.sub('[\(\[].*?[\)\]]', '', line))
        return Formatter.get_script_list(ret)

    def get_char_tokens(self, person):
        ret = []
        for col in self.script_map:
            if col['person'].upper() == person.upper():
                ret += Utils.get_token(col['text'])
        return ret

    def get_characters(self):
        ret = []
        for col in self.script_map:
            ret.append(col['person'])
        return list(dict.fromkeys(ret))  # remove redundancies

    def get_tokens(self):
        ret = []
        for col in self.script_map:
            ret += Utils.get_token(col['text'])  # col['text'].lower().split()
        return ret

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

