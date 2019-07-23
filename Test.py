import string

from Utilities import Utils
import itertools
from Formatter1 import Formatter as FirstFormatter
from Formatter2 import Formatter as SecondFormatter
from Formatter3 import Formatter as ThirdFormatter
from Formatter4 import Formatter as FourthFormatter
from Formatter5 import Formatter as FifthFormatter
from Formatter6 import Formatter as SixthFormatter
from gensim.models import Word2Vec as wv, Word2Vec
from gensim.models import KeyedVectors as kv
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from prettytable import PrettyTable

model = kv.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
utils = Utils()

stop_words = ["i", "i'm", "it's", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
              "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
              "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
              "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
              "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
              "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during",
              "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
              "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any",
              "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
              "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
non_feminist_words = ['boys ', 'hope ', 'hungry?', 'dress', 'shoes', 'cleaning', 'cooking', 'gentle', 'passive', 'indecisive', 'babyish',
                      'brainless', 'miserable', 'naive', 'needy', 'obsessive', 'insecure', 'weak', 'wicked',
                      'accepting', 'adorable', 'caring', 'curvy', 'cute', 'darling', 'dramatic', 'dreaming', 'dreamy',
                      'kind', 'likable', 'lovable', 'loved', 'loving', 'natural', 'nice', 'petite', 'polite',
                      'precious', 'pretty', 'sacrificing', 'emotional', 'feminine', 'fit', 'foxy', 'gentle', 'giggly',
                      'girly', 'hot', 'innocent', 'sensitive', 'sensual', 'soft', 'sweet', 'thin', 'vulnerable',
                      'womanly', 'shy']
feminist_words = ['here', 'go', 'lets', 'Full ', 'Go', 'secure', 'funny', 'fun', 'extraordinary', 'adventurous', 'leader', 'focused', 'stable', 'curious',
                  'loud', 'logical', 'ambitious', 'cynical', 'assertive', 'bright', 'fight', 'experienced',
                  'charismatic', 'resentful', 'liberal', 'free', 'eccentric', 'educated', 'think', 'want', 'brave',
                  'busy', 'brilliant', 'masculine', 'Strong', 'tough', 'protective', 'hero', 'powerful', 'aggressive',
                  'smart', 'intelligent', 'books', 'independent', 'leader', 'manager', 'active', 'arrogant', 'dominant']
men_words = ['he', 'men', 'man,''himself', 'boy', 'son', 'his', 'guy', 'father']
women_words = ['she', 'women', 'woman', 'herself', 'girl', 'daughter', 'gal', 'mother']


def safe_model_similarity(x, y):
    try:
        return model.similarity(x, y)
    except KeyError:
        return -1


def get_feminist_score(word, lst):
    similarity = [safe_model_similarity(word, feminist_word) for feminist_word in lst]
    similarity = [x for x in similarity if x == x and x != -1 if x > 0.1]
    if len(similarity) > 0:
        return np.max(similarity)
    return 0


def expand_list(word_list):
    word_list = [x for x in word_list if model.similarity('hello', x) != -1]  # word exist in corpus
    expanded = [[i[0] for i in model.similar_by_word(word, 5)] for word in word_list]
    word_list = word_list + list(np.array(expanded).flatten())
    return list(set(list(word_list)))


def all_scripts_except_one():
    for to_remove_movie in utils.names:
        str = ""
        for name in utils.names:
            if name != to_remove_movie:
                my_movie = get_formatter(name)
                str = str + " ".join(my_movie.get_tokens()) + "\n"
        f = open("scripts_without_" + to_remove_movie + ".txt", "w", encoding='utf-8')
        f.write(str)
        f.close()


def females():
    return ['Jessie', 'Bonnie', 'Bonnie', 'Emily', 'HOLLEY', 'SALLY',
            'DORY', 'PEACH', 'Alice', 'Queen', 'Duchess', 'Madame', 'Marie', 'Amelia', 'Abigail',
            'Catty', 'Matriarch', 'Joy', 'Sadness', 'Disgust', 'Mom', 'Riley', 'Sally Carrera', 'Flo',
            'Cruella de Vil', 'Nanny', 'Perdita', 'Anita',
            'Elinor', 'Merinda', 'The Witch', 'Moana', 'Sina', 'Gramma', 'Mulan', 'Granny Fa',
            'Ursula', 'Ariel', 'POCAHONTAS', 'GRANDMOTHER WILLOW', 'POCAHONTAS I', 'NAKOMA',
            'ANNA', 'ELSA', 'YOUNG ANNA', 'MRS. DAVIS', 'BO PEEP', 'HANNAH', 'HOPPS',
            'BELLWETHER', 'BONNIE HOPPS', 'YOUNG JUDY', 'FRU FRU SHREW', 'GAZELLE', 'JASMINE',
            'BELLE', 'MRS.POTTS', 'Megara', 'Akela', 'Flora', 'Maleficent',
            'Merryweather', 'Fauna', 'Briar Rose', 'Fairies']


def get_number_of_woman_words_in_script(movie):
    this_females = females()
    this_females = list(map(lambda x: x.lower(), this_females))
    return np.sum([character[1] for character in movie.get_chars_tuples() if character[0].lower() in this_females])

def get_number_of_words_in_script(movie):
    this_females = females()
    this_females = list(map(lambda x: x.lower(), this_females))
    this_males = males()
    this_males = list(map(lambda x: x.lower(), this_males))
    return np.sum([character[1] for character in movie.get_chars_tuples() if (character[0].lower() in this_females or character[0].lower() in this_males)])



def change_range(oldValue):
    return (((oldValue - -1) * (5 - 0)) / (1 - -1)) + 0


def get_feminism_score(words_lst, character_words):
    score = [get_feminist_score(word, words_lst) for word in character_words]
    score = [x for x in score if x == x and x > 0.1]
    return np.mean(score) if len(score) > 0 else 0


arr = []


def get_meaning_score(name):
    my_movie = get_formatter(name)
    movie_characters = my_movie.get_characters()
    movie_characters = list(map(lambda x: x.lower(), movie_characters))
    character_scores = []
    this_females = females()
    this_females = list(map(lambda x: x.lower(), this_females))
    for character in movie_characters:
        if character.lower() in this_females:
            words = my_movie.get_char_tokens(character.lower())
            character_words = [w for w in words if w not in stop_words]
            not_feminist_score = get_feminism_score(non_feminist_words, character_words)
            feminist_score = get_feminism_score(feminist_words, character_words)

            arr.append([character, (feminist_score - not_feminist_score)])
            character_scores.append(
                (feminist_score - not_feminist_score) * len(words) /
                (get_number_of_words_in_script(my_movie)))
    return change_range(np.sum(character_scores))


def get_k_most_similar_to_list(k, lst, words):
    similarities_to_men = [[word, np.mean([safe_model_similarity(men_word, word) for men_word in lst])] for word in
                           words]
    return [i[0] for i in sorted(similarities_to_men, key=lambda x: x[1], reverse=True) if i[1] != -1][:k]


# feminist words are related to man or woman more?
def is_disney_corpus_biased():
    words = feminist_words + non_feminist_words
    men_similarity = get_k_most_similar_to_list(10, men_words, words)
    women_similarity = get_k_most_similar_to_list(10, women_words, words)
    print(men_similarity)
    print(women_similarity)
    men_score = [x for x in men_similarity if x in feminist_words]
    women_score = [x for x in women_similarity if x in feminist_words]
    return len(women_score) - len(men_score)


def is_movie_feminist(name):
    my_movie = get_formatter(name)
    words = my_movie.get_tokens()
    non_feminist_score = get_feminism_score(non_feminist_words, words)
    feminist_score = get_feminism_score(feminist_words, words)
    return feminist_score - non_feminist_score


def create_word2vec_model_from_scripts():
    sentences = []

    for name in utils.names:
        if name != 'Kung Fu Panda':
            my_movie = get_formatter(name)
            sentences = sentences + [x['text'].translate(str.maketrans("", "", string.punctuation)).split(" ")[:-1] for
                                     x in
                                     my_movie.script_map]
    sentences = [[x for x in sentence if x not in stop_words] for sentence in sentences]
    model = Word2Vec(sentences, min_count=1)
    return model


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()
    plt.savefig('testplot.png')


def get_formatter(name):
    tmp = Utils.formatter(name)
    return FirstFormatter(name) if tmp == '1' else \
        SecondFormatter(name) if tmp == '2' else \
        ThirdFormatter(name) if tmp == '3' else \
        FourthFormatter(name) if tmp == '4' else  \
        FifthFormatter(name) if tmp == '5' else SixthFormatter(name)

def get_female_part(chars_map, females, males):
    females_sum = 0
    sum = 0
    for key, val in chars_map:
        if key.lower() in females:
            # print(key, "==", val)
            females_sum += val
            sum += val
        if key in males:
            sum += val
    return females_sum / sum

def bechdelTest(arr, females, males):
    this_females = []
    test2 = False
    prev_preson = None
    prev_text = None
    for curMap in arr:
        for key, value in curMap.items():
            if key == 'person':
                person = value.lower()
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
                    if (male in text.lower()) or (male in prev_text.lower()):
                        test3 = False
                male_words = ['him', 'he', 'himself', 'his', 'man', 'male', 'boy', 'guy', 'son']
                for word in male_words:
                    if (word in text.lower()) or (word in prev_text.lower()):
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

def males():
    return ['MATER', 'MCQUEEN', 'FRANCESCO', 'SARGE', 'BRENT MUSTANGBURGER', 'PROFESSOR ZUNDAPP', 'MILES AXLEROD',
            'TOMBER', 'GREM', 'ACER', 'UNCLE TOPOLINO', 'ROD REDLINE', 'VLADIMIR TRUNKOV', 'CRABBY',
            'Lightning McQueen', 'Tow Mater', 'Doc Hudson', 'Bob Cutlass', 'Luigi', 'Darrell Cartrip',
            'Chick', 'Sheriff', 'Mack', 'Lizzie', 'Ramone', 'The King', 'Cameramen', 'Sarge', 'Van',
            'Bing Bong', 'Fear', 'Anger', 'Dad', 'Timothy Q. Mouse', 'Ringmaster', 'Mr. Stork',
            "O'Malley", 'Edgar', 'Roquefort', 'Napoleon', 'Berlioz', 'Toulouse', 'Georges', 'Lafayette', 'Scat Cat',
            'White Rabbit', 'Mad Hatter', 'Dodo', 'March Hare', 'Cheshire Cat', 'Walrus', 'Caterpillar', 'Doorknob', 'King',
            'Marlin', 'GILL', 'NEMO', 'NIGEL', 'SHERMAN', 'BRUCE', 'CRUSH', 'BLOAT', 'GURGLE', 'MOONFISH', 'Coral', 'CHUM',
            'Pongo', 'Jasper', 'Roger', 'Colonel', 'Sergeant Tibbs', 'Horace', 'Patch', 'Danny',
            'JOHN SMITH', 'RATCLIFFE', 'POWHATAN', 'BEN', 'THOMAS', 'LON', 'WIGGINS',
            'Maui', 'Tamatoa', 'Tui', 'Fergus', 'Mr. Potato Head', 'Wheezy', 'Ken', 'Chuckles', 'Lotso',
            'Mushu', 'Shang', 'Chi Fu', 'Emperor', 'Shan Yu', 'General', 'Yao', 'Ling',
            'Scuttle', 'Eric', 'Triton', 'Grimsby', 'Flounder', 'Sebastian', 'KRISTOFF', 'OLAF', 'HANS', 'DUKE',
            'GRAND PABBIE', 'OAKEN', 'WOODY', 'BUZZ', 'SID', 'Al', 'Stinky Pete', 'Utility Belt Buzz',
            'REX', 'SARGENT', 'ANDY', 'HAMM', 'SLINKY', 'NICK', 'BOGO', 'STU HOPPS', 'CLAWHAUSER',
            'LIONHEART', 'DUKE WEASELTON', 'GIDEON GREY', 'YAX THE HIPPIE YAK', 'YAX',
            'ALADDIN', 'GENIE', 'JAFAR', 'SULTAN', 'IAGO', 'PEDDLER', 'COGSWORTH', 'GASTON',
            'LUMIERE', 'BEAST', 'MAURICE', 'LEFOU', 'CHIP', 'Hercules', 'Hades', 'Phil', 'Zeus', 'Pain',
            'Panic', 'Man', 'Amphitryon', 'Hermes', 'Atropos', 'Baloo', 'Bagheera', 'Mowgli', 'Hathi',
            'Buzzy', 'Kaa', 'Shere Khan', 'Louie', 'Flaps', 'Dizzy', 'Hathi Jr.', 'Hubert', 'Phillip', 'Stefan']


def get_movie_rate(name):
    my_movie = get_formatter(name)
    movie_arr = my_movie.script_map
    chars_arr = my_movie.get_chars_tuples()
    rate = 0
    this_females = females()
    this_females = list(map(lambda x: x.lower(), this_females))
    this_males = males()
    this_males = list(map(lambda x: x.lower(), this_males))
    rate += ((bechdelTest(movie_arr, this_females, this_males) / 3) * 2)
    rate += ((get_female_part((chars_arr), this_females, this_males)) * 3)
    female_meaning = get_meaning_score(name)
    # return rate, female_meaning
    return 0, female_meaning

def get_year(name):
    yearMap = {'Frozen': 2013, 'Toy Story': 1995, 'Zootopia': 2016, 'Aladdin': 1992,
               'Beauty and the Beast': 1991, 'Hercules': 1997, 'Jungle Book': 1967, 'Sleeping Beauty': 1959,
               'Brave': 2012, 'Moana': 2016, 'Mulan': 1998, 'The Little Mermaid': 1989, 'Pocahonta': 1995}
    return yearMap[name]



if __name__ == '__main__':
    # model = create_word2vec_model_from_scripts()
    # for name in utils.names:
    #     print(name)
    #     my_movie = get_formatter(name)
    #     # print(my_movie.get_characters())
    #     print(my_movie.get_chars_tuples())
    #
    movies = utils.data['movies']
    meaning_rates = []
    years = []
    final_names = []
    rates = []
    for movie in movies:
        my_movie = get_formatter(movie['name'])
        name = movie['name']
        this_rate, meaning = get_movie_rate(name)
        meaning_rates.append(meaning)
        rates.append(this_rate)
        years.append(movie['year'])
        final_names.append(name)

    print(meaning_rates)

    min_meaning = np.asarray(meaning_rates).min()
    meaning_rates = list(map(lambda x: (x - min_meaning), meaning_rates))
    print(meaning_rates)

    max_meaning = np.asarray(meaning_rates).max()
    meaning_rates = list(map(lambda x: ((x / max_meaning) * 5), meaning_rates))
    print(meaning_rates)
    t = PrettyTable(['Name', 'Meaning'])

    for i in range(0, len(rates)):
        rates[i] += meaning_rates[i]
        t.add_row([final_names[i], rates[i]])

    print(t)

    for i in range(0, len(final_names)):
        print(final_names[i], " - ", rates[i])

    fig, ax = plt.subplots()
    colors = np.random.rand(len(years))
    area = (100 * np.random.rand(len(years)))
    ax.scatter(years, rates, s=area, c=colors, alpha=0.5)
    # ax.set_facecolor('xkcd: white')
    ax.grid()

    for i, txt in enumerate(final_names):
        ax.annotate(txt, (years[i], rates[i]))

    z = np.polyfit(years, rates, 1)
    p = np.poly1d(z)
    print(p)

    plt.plot(years, p(years), color=(0.2, 0.4, 0.6, 0.6))

    plt.show()

        # print(my_movie.script_map)
    # print(is_disney_corpus_biased())
    # arr2 = [[name, get_meaning_score(name)] for name in utils.names]
    # print (sorted(arr2, key=lambda x:x[1], reverse=True))
    #
    # print (sorted(arr, key=lambda x:x[1], reverse=True))

    #     print (name, is_movie_feminist(name))
    # # model.save("frozen_model.bin")

    # print(is_disney_corpus_biased())
