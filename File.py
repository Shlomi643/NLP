import nltk
import FirstFormatter as ff
import SecondFormatter as sf
from bs4 import BeautifulSoup as bs
from nltk.corpus import stopwords
from gensim.models import Word2Vec as wv
from nltk.tokenize import sent_tokenize
from os import listdir
from os.path import isfile, join


filesMap = {}
funcs = {}
names = []


def set_s(format_index, name):
    return ff if format_index == '1' else sf, open("Scripts/Format " + format_index + "/" + name + ".html").read()


def build_map(path):
    my_dir = "Scripts/" + path
    files = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    for f in files:
        file_name = f[0:f.index('.html')]
        names.append(file_name)
        # print(file_name)
        filesMap[file_name] = set_s(my_dir[-1], file_name)


def script(name):
    return filesMap[name][1]


def formatter(name):
    return filesMap[name][0]


def get(name):
    return funcs[name]


def my_soup(x):
    return bs(script(x), 'html.parser')


def init_map():
    build_map("Format 1")
    build_map("Format 2")
    funcs['char_tokens'] = lambda x: lambda y: getattr(formatter(x), 'get_char_tokens')(my_soup(x), y)
    funcs['script_map'] = lambda x: getattr(formatter(x), 'get_script_map')(my_soup(x))
    funcs['all_tokens'] = lambda x: getattr(formatter(x), 'get_tokens')(my_soup(x))
    funcs['get_words_num'] = lambda x: getattr(formatter(x), 'get_words_num')(my_soup(x))
    funcs['get_characters'] = lambda x: getattr(formatter(x), 'get_characters')(my_soup(x))


def func():
    file = open("Scripts/Format 2/Beauty and the Beast.html", "r")
    file_text = file.read()
    soup = bs(file_text, 'html.parser')
    script_map = sf.get_script_map(soup)
    belle_tokens = sf.get_tokens(script_map)
    tokens = map(lambda x: sent_tokenize(x), belle_tokens)
    freq = nltk.FreqDist([x for x in belle_tokens if x not in stopwords.words('english')])
    # print(english_stopwords)
    # for key, val in freq.items():
    #     print((str(key) + ':' + str(val)))
    model = wv(tokens, min_count=1, size=100, window=5)
    # print(belle_tokens)
    print("Cosine similarity between 'prince' " +
          "and 'young' - CBOW : ",
          model.similarity('man', 'beauty'))
    freq.plot(40, cumulative=False)


def mmm(name):
    return lambda x: get(x)(name)


if __name__ == '__main__':
    init_map()
    # print(names)

    for name in names:
        my_movie = mmm(name)
        print(name)
        print(my_movie('get_characters'))
        # print(" ".join(my_movie('all_tokens')))
        # print(my_movie('get_words_num'))
        print()

    # print(filesMap)
