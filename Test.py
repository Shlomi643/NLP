import string

from Utilities import Data
import itertools
from FF import FirstFormatter
from SF import SecondFormatter
from gensim.models import Word2Vec as wv, Word2Vec
from gensim.models import KeyedVectors as kv
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

model = kv.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
utils = Data()

stop_words = ["i", "i'm", "it's" ,"me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
non_feminist_words = ['dress', 'shoes', 'cleaning', 'cooking', 'gentle', 'passive', 'indecisive', 'babyish', 'brainless', 'miserable', 'naive', 'needy', 'obsessive', 'insecure', 'weak', 'wicked','accepting', 'adorable', 'caring', 'curvy', 'cute', 'darling', 'dramatic', 'dreaming', 'dreamy', 'kind',  'likable', 'lovable', 'loved', 'loving', 'natural', 'nice', 'petite', 'polite', 'precious', 'pretty', 'sacrificing', 'emotional', 'feminine', 'fit', 'foxy', 'gentle', 'giggly', 'girly', 'hot', 'innocent', 'sensitive', 'sensual',  'soft', 'sweet', 'thin', 'vulnerable',  'womanly', 'shy']
feminist_words = ['secure','funny', 'fun', 'extraordinary', 'adventurous', 'leader', 'focused', 'stable', 'curious', 'loud', 'logical', 'ambitious', 'cynical', 'assertive', 'bright', 'fight', 'experienced', 'charismatic', 'resentful', 'liberal', 'free', 'eccentric', 'educated', 'think', 'want', 'brave', 'busy', 'brilliant', 'masculine', 'Strong', 'tough', 'protective', 'hero', 'powerful', 'aggressive', 'smart', 'intelligent', 'books', 'independent', 'leader', 'manager', 'active', 'arrogant', 'dominant']
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
    if len(similarity)>0:
        return np.max(similarity)
    return 0


def expand_list(word_list):
    word_list = [x for x in word_list if model.similarity('hello', x)!=-1] #word exist in corpus
    expanded = [[i[0] for i in model.similar_by_word(word, 5)] for word in word_list ]
    word_list = word_list + list(np.array(expanded).flatten())
    return list(set( list(word_list)))


def all_scripts_except_one():
    for to_remove_movie in utils.names:
        str = ""
        for name in utils.names:
            if name != to_remove_movie:
                my_movie= FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
                str = str + " ".join(my_movie.get_tokens()) + "\n"
        f = open("scripts_without_"+to_remove_movie+".txt", "w", encoding='utf-8')
        f.write(str)
        f.close()

def females():
    return ['ANNA', 'ELSA', 'YOUNG ANNA', 'MRS. DAVIS', 'BO PEEP', 'HANNAH', 'HOPPS',
            'BELLWETHER', 'BONNIE HOPPS', 'YOUNG JUDY', 'FRU FRU SHREW', 'GAZELLE', 'JASMINE',
            'BELLE', 'MRS.POTTS', 'Megara', 'Akela', 'Flora', 'Maleficent',
            'Merryweather', 'Fauna', 'Briar Rose', 'Fairies']


def get_number_of_woman_words_in_script(movie):
    return np.sum([character[1] for character in movie.get_chars_tuples() if character[0] in females()])


def change_range(oldValue):
    return (((oldValue - -1) * (5 - 0)) / (1 - -1)) + 0


def get_feminism_score( words_lst, character_words):
    score = [get_feminist_score(word, words_lst) for word in character_words]
    score = [x for x in score if x == x and x > 0.1]
    return np.mean(score) if len(score) > 0 else 0


arr = []
def get_meaning_score(name):
    my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
    movie_characters = my_movie.get_characters()
    character_scores = []
    for character in movie_characters:
        if character in females():
            words = my_movie.get_char_tokens(character)
            character_words = [w for w in words if w not in stop_words]
            not_feminist_score = get_feminism_score(non_feminist_words, character_words)
            feminist_score = get_feminism_score(feminist_words, character_words)

            arr.append([character, (feminist_score - not_feminist_score)])
            character_scores.append(
                (feminist_score - not_feminist_score) * len(words) / get_number_of_woman_words_in_script(my_movie))
    return change_range(np.sum(character_scores))


def get_k_most_similar_to_list(k,lst, words):
    similarities_to_men = [[word,np.mean([safe_model_similarity(men_word,word) for men_word in lst])] for word in words]
    return [i[0] for i in sorted(similarities_to_men, key=lambda x:x[1], reverse=True) if i[1]!=-1][:k]

# feminist words are related to man or woman more?
def is_disney_corpus_biased():

    words = feminist_words + non_feminist_words
    men_similarity = get_k_most_similar_to_list(10, men_words, words)
    women_similarity = get_k_most_similar_to_list(10, women_words, words)
    print (men_similarity)
    print (women_similarity)
    men_score = [x for x in men_similarity if x in feminist_words]
    women_score = [x for x in women_similarity if x in feminist_words]
    return len(women_score) - len(men_score)


def is_movie_feminist(name):
    my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
    words = my_movie.get_tokens()
    non_feminist_score = get_feminism_score(non_feminist_words, words)
    feminist_score = get_feminism_score(feminist_words, words)
    return feminist_score - non_feminist_score


def create_word2vec_model_from_scripts():
    sentences = []

    for name in utils.names:
        if name!= 'Kung Fu Panda':
            my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
            sentences = sentences + [x['text'].translate(str.maketrans("", "", string.punctuation)).split(" ")[:-1] for x in
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


if __name__ == '__main__':

    model = create_word2vec_model_from_scripts()
    print(is_disney_corpus_biased())
    # arr2 = [[name, get_meaning_score(name)] for name in utils.names]
    # print (sorted(arr2, key=lambda x:x[1], reverse=True))
    #
    # print (sorted(arr, key=lambda x:x[1], reverse=True))

    #     print (name, is_movie_feminist(name))
    # # model.save("frozen_model.bin")


    # print(is_disney_corpus_biased())




