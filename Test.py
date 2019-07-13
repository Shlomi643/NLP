from Utilities import Data
import itertools
from FF import FirstFormatter
from SF import SecondFormatter
from gensim.models import Word2Vec as wv
from gensim.models import KeyedVectors as kv
import numpy as np

# model = kv.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
utils = Data()

stop_words = ["i", "i'm", "it's" ,"me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
feminist_words = ['masculine','Strong','tough','protective','hero','powerful','aggressive','smart','intelligent','books','independent','leader','manager','active','arrogant','dominant']
non_feminist_words = ['dress', 'makeup','shoes','cleaning', 'cooking','kitchen','homemaker','baker','secretary','gentle','housekeeper', 'nanny','baker','passive','indecisive','sexy','immature','shy','abusive', 'babyish', 'bitchy', 'brainless',
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
            character_scores.append(
                (feminist_score - not_feminist_score) * len(words) / get_number_of_woman_words_in_script(my_movie))
    return change_range(np.sum(character_scores))


if __name__ == '__main__':
    for name in utils.names:
        my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
        # print(get_meaning_score(name))/
        if name == 'Sleeping Beauty':
            chars = my_movie.get_characters()
            for char in chars:
                print(char)
                print(my_movie.get_char_tokens(char))

