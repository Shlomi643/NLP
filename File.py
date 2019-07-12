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

model = kv.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
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


stop_words = ["i", "i'm", "it's" ,"me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
non_feminist_words = ['cleaning', 'cooking','kitchen','homemaker','baker','secretary','gentle','housekeeper', 'nanny','baker','passive','indecisive','sexy','immature','shy']
feminist_words = ['Strong','tough','protective','hero','powerful','aggressive','smart','intelligent','books','independent','leader','mangaer','active','arrogant','dominant']

# if __name__ == '__main__':
#     init_map()
#     # print(names)
#     my_movie = mmm('Frozen')
#     words = my_movie('char_tokens')('Elsa')
#     filtered_sentence = [w for w in words if w not in stop_words]
#     for word in filtered_sentence:
#         for feminist_word in feminist_words:
#             model.similarity(word,)


    # test()
    # init_map()
    # # print(names)
    # # get_corpus(True)
    # for name in names:
    #     my_movie = mmm(name)
    #     print(name)
    #     for char in my_movie('get_characters'):
    #         print(char)
    #         print(my_movie('char_tokens')(char))
    #     # print(my_movie('get_characters'))
    #     # print(" ".join(my_movie('all_tokens')))
    #     # print(my_movie('get_words_num'))
    #     # print()
    #
    # # print(filesMap)
    # # print(len(get_corpus_list()))
