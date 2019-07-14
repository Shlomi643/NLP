# import gensim
import nltk
import numpy as np
import itertools
import FirstFormatter as ff
import SecondFormatter as sf
from bs4 import BeautifulSoup as bs
from nltk.corpus import stopwords
from gensim.models import Word2Vec as wv
from gensim.models import KeyedVectors as kv
from nltk.tokenize import sent_tokenize
from os import listdir
from os.path import isfile, join
from sklearn.neighbors import KNeighborsClassifier

# model = kv.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
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


def get_female_part(chars_map, females, males):
    females_sum = 0
    sum = 0
    for key, val in chars_map:
        if key in females:
            females_sum += val
            sum += val
        if key in males:
            sum += val
    return females_sum / sum

def get_movie_rate(name):
    my_movie = mmm(name)
    movie_arr = my_movie('script_map')
    chars_arr = my_movie('get_chars_tuples')
    rate = 0
    rate += ((bechdelTest(movie_arr, females(), males()) / 3) * 2)
    rate += ((get_female_part((chars_arr), females(), males())) * 3)
    
    return rate

def get_year(name):
    yearMap = {'Frozen': 2013, 'Toy Story': 1995, 'Zootopia': 2016, 'Aladdin': 1992,
               'Beauty and the Beast': 1991, 'Hercules': 1997, 'Jungle Book': 1967, 'Sleeping Beauty': 1959}
    return yearMap[name]

def get_corpus(to_write):
    to_print = ''
    for n in names:
        mmovie = mmm(n)
        to_print += " ".join(mmovie('all_tokens')) + '\n'
    print(to_print)
    f = open("Monet.txt", "w", encoding='utf-8')
    if not to_write:
        return
    f.write(to_print)
    f.close()


def get_corpus_list():
    ret = []
    for n in names:
        mmovie = mmm(n)
        ret.append(mmovie('all_tokens'))
    return ret


# x - y -> x


def print_sim(w1, w2):
    print("Cosine similarity between '" + w1 + "' " +
          "and '" + w2 + "' - CBOW : ", model.similarity(w1.lower(), w2.lower()))


def temp(x, y):
    try:
        return model.similarity(x, y)
    except KeyError:
        return 0


def get_means(arr1, arr2):
    return [(temp(x, y)) for x, y in itertools.product(arr1, arr2)]
    # print([model.similarity(x, y) for x, y in zip(arr1, arr2)])


def get_mean(arr1, arr2):
    return np.mean(get_means(arr1, arr2))


def get_all_tokens():
    ret = []
    for name in names:
        my_movie = mmm(name)
        toapp = []
        for char in my_movie('get_characters'):
            tokens = my_movie('char_tokens')(char)
            def mean(x): get_mean(tokens, x)
            toapp.append({'character': char, 'male': mean(men_stuff), 'female': mean(women_stuff)})
        ret.append({'movie': name, 'male': get_mean(my_movie('all_tokens'), men_stuff), 'female': get_mean(my_movie('all_tokens'), women_stuff), 'characters': toapp})
    return ret


def test():
    # model
    men_stuff = ['guy', 'man', 'men', 'he', 'his', 'himself', 'boy', 'male']
    women_stuff = ['gal', 'woman', 'women', 'she', 'her', 'herself', 'girl', 'female']
    mmovie = mmm('Beauty and the Beast')
    tokenn = mmovie('char_tokens')('Belle')
    # print(np.mean([model.similarity(i, 'pretty') for i in men_stuff]))
    # print(np.mean([model.similarity(i, 'pretty') for i in women_stuff]))
    print(get_means(men_stuff, tokenn))
    print(get_means(women_stuff, tokenn))
    print(np.mean(men_stuff))
    print(np.mean(women_stuff))

    print_sim('Beauty', 'She')
    print_sim('Beauty', 'Woman')
    print_sim('Beauty', 'Girl')
    print_sim('Beauty', 'Pretty')
    print_sim('Beauty', 'Man')
    print_sim('Beauty', 'man')
    print_sim('Beauty', 'Guy')
    print_sim('Beauty', 'Boy')


if __name__ == '__main__':
    # test()
    init_map()
    # print(names)
    # get_corpus(True)
    for name in names:
        if name != 'Cars 2' and name != 'Kung Fu Panda':
            if name == 'Sleeping Beauty':
                rate.append(get_movie_rate(name))
                years.append(get_year(name))
                final_names.append(name)
            else:
                rate.append(get_movie_rate(name) + 5)
                years.append(get_year(name))
                final_names.append(name)


    # plt.scatter(years, rate)
    # z = numpy.polyfit(years, rate, 1)
    # p = numpy.poly1d(z)
    # print(p)
    # plt.plot(years, p(years), "r-")
    # plt.show()
    # my_movie = mmm(name)
        # print(name)
        # print(my_movie('script_map'))
        # print(" ".join(my_movie('all_tokens')))
        # print(my_movie('get_words_num'))
        # print()

    # print(filesMap)
    # print(len(get_corpus_list()))
