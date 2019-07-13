# import gensim
import nltk
from blaze.compute.tests.test_numpy_compute import ax

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
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

model = kv.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
filesMap = {}
funcs = {}
names = []
females = []
males = []

def get_female_adj():
    return ['abusive', 'babyish', 'bitchy', 'brainless',
            'compulsive', 'crazy', 'ditzy', 'dumb', 'empty',
            'foolish', 'fussy', 'gold digging', 'gossipy',
            'hot tempered', 'ignorant', 'irresponsible', 'jealous',
            'lazy', 'lonely', 'mean', 'miserable', 'misguided', 'naive', 'narrow-minded', 'naughty', 'needy',
            'nosy', 'obnoxious', 'obsessive', 'fake', 'foolish', 'insane',
            'insecure', 'shallow', 'weak', 'wicked', 'witchy', 'wretched', 'accepting'
            , 'adorable', 'careful', 'caring', 'charming', 'cheeky', 'curvy', 'cute'
            , 'darling', 'dramatic', 'dreaming', 'dreamy', 'joyful'
            , 'kind', 'kind-hearted', 'kissable', 'ladylike', 'likable'
            , 'lovable', 'loved', 'lovely', 'loving', 'natural', 'nice'
            , 'petite', 'polite', 'precious', 'pretty', 'romantic'
            , 'sacrificing', 'sassy', 'easy-going', 'emotional'
            , 'female', 'feminine', 'fit', 'foxy', 'gentle'
            , 'giggly', 'girly', 'giving', 'hot', 'innocent'
            , 'intimate', 'sensitive', 'sensual', 'sexual', 'sexy'
            , 'shy', 'skinny', 'soft', 'soft-spoken', 'sweet'
            , 'thin', 'vunerable', 'warm', 'willing', 'witty'
            , 'womanly', 'wonderful', 'young', 'youthful']

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

def females():
    return ['ANNA', 'ELSA', 'YOUNG ANNA', 'MRS. DAVIS', 'BO PEEP', 'HANNAH', 'HOPPS',
            'BELLWETHER', 'BONNIE HOPPS', 'YOUNG JUDY', 'FRU FRU SHREW', 'GAZELLE', 'JASMINE',
            'BELLE', 'MRS.POTTS', 'Megara', 'Akela', 'Flora', 'Maleficent',
            'Merryweather', 'Fauna', 'Briar Rose', 'Fairies']

def males():
    return ['KRISTOFF', 'OLAF', 'HANS', 'DUKE', 'GRAND PABBIE', 'OAKEN', 'WOODY', 'BUZZ', 'SID',
            'REX', 'SARGENT', 'ANDY', 'HAMM', 'SLINKY', 'NICK', 'BOGO', 'STU HOPPS', 'CLAWHAUSER',
            'LIONHEART', 'DUKE WEASELTON', 'GIDEON GREY', 'YAX THE HIPPIE YAK', 'YAX',
            'ALADDIN', 'GENIE', 'JAFAR', 'SULTAN', 'IAGO', 'PEDDLER', 'COGSWORTH', 'GASTON',
            'LUMIERE', 'BEAST', 'MAURICE', 'LEFOU', 'CHIP', 'Hercules', 'Hades', 'Phil', 'Zeus', 'Pain',
            'Panic', 'Man', 'Amphitryon', 'Hermes', 'Atropos', 'Baloo', 'Bagheera', 'Mowgli', 'Hathi',
            'Buzzy', 'Kaa', 'Shere Khan', 'Louie', 'Flaps', 'Dizzy', 'Hathi Jr.', 'Hubert', 'Phillip', 'Stefan']

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
    funcs['get_chars_tuples'] = lambda x: getattr(formatter(x), 'get_chars_tuples')(my_soup(x))
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

def bechdelTest(arr, females, males):
    this_females = []
    test2 = False
    prev_preson = None
    prev_text = None
    for curMap in arr:
        for key, value in curMap.items():
            if key == 'person':
                person = value
            else:
                text = value
        if not prev_preson:
            if person in females:
                this_females.append(person)
            prev_preson = person
            prev_text = text
        else:
            if person in females and person not in this_females:
                this_females.append(person)
            if (person != prev_preson) and (person in females) and (prev_preson in females):
                test2 = True
                test3 = True
                for male in males:
                    if (male in text) or (male in prev_text):
                        test3 = False
                male_words = ['him', 'he', 'himself', 'his', 'man', 'male', 'boy', 'guy', 'son']
                for word in male_words:
                    if (word in text) or (word in prev_text):
                        test3 = False
                if test3:
                    # print("\n", person, '\ntext1 -', text, "\n", prev_preson, "\ntext2 -", prev_text)
                    return 3
            prev_preson = person
            prev_text = text
    if len(this_females) < 2:
        return 0
    if test2:
        return 2
    return 1

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
    init_map()
    # print(names)
    # get_corpus(True)
    rate = []
    years = []
    final_names = []
    for name in names:
        if name != 'Cars 2' and name != 'Kung Fu Panda':
            rate.append(get_movie_rate(name))
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

    fig, ax = plt.subplots()
    # colors = np.random.rand(len(years))
    # area = (100 * np.random.rand(len(years)))
    ax.scatter(years, rate,
               #s=area, c=colors,
               alpha=0.5)
    ax.set_facecolor('xkcd:powder blue')
    ax.grid()

    for i, txt in enumerate(final_names):
        ax.annotate(txt, (years[i], rate[i]))

    z = np.polyfit(years, rate, 1)
    p = np.poly1d(z)
    print(p)

    plt.plot(years, p(years), "r-")

    plt.show()

    # print(filesMap)
    # print(len(get_corpus_list()))
