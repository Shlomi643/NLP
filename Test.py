from File import mmm
from Utilities import Data
import itertools
from FF import FirstFormatter
from SF import SecondFormatter
from gensim.models import Word2Vec as wv
from gensim.models import KeyedVectors as kv
import numpy as np

model = kv.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
utils = Data()

stop_words = ["i", "i'm", "it's" ,"me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
non_feminist_words = ['cleaning', 'cooking','kitchen','homemaker','baker','secretary','gentle','housekeeper', 'nanny','baker','passive','indecisive','sexy','immature','shy']
feminist_words = ['masculine','Strong','tough','protective','hero','powerful','aggressive','smart','intelligent','books','independent','leader','manager','active','arrogant','dominant']


def safe_model_similarity(x, y):
    try:
        return model.similarity(x, y)
    except KeyError:
        return -1


def get_feminist_score(word, lst):
    similarity = [safe_model_similarity(word, feminist_word) for feminist_word in lst]
    return np.max([x for x in similarity if x == x and x != -1 if x > 0.1])


def expand_list(word_list):
    word_list = [x for x in word_list if model.similarity('hello', x)!=-1] #word exist in corpus
    expanded = [[i[0] for i in model.similar_by_word(word, 5)] for word in word_list ]
    word_list.append(np.array(expanded).flatten())
    return list(set(list(word_list)))


if __name__ == '__main__':
    print(expand_list(feminist_words))
    # for name in utils.names:
    #     my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
    #     movie_characters = my_movie.get_characters()
    #     print ("****************************", name)
    #     for character in movie_characters:
    name = 'Frozen'
    character = 'Elsa'
    my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)

    words = my_movie.get_char_tokens(character)
    character_words = [w for w in words if w not in stop_words]
    non_feminists = [get_feminist_score(word, non_feminist_words) for word in character_words]
    non_feminists = [x for x in non_feminists if x == x and x > 0.1]
    feminists = [get_feminist_score(word, feminist_words) for word in character_words]
    feminists = [x for x in feminists if x==x and x>0.1]
    print (character, "\n", "feminist score:", np.mean(feminists), "\nnon feminist score:", np.mean(non_feminists),"\n")
print ("\n\n\n")



    # for word in character_words:
            #     print('word:', word)
            #     feminist_similarity = [safe_model_similarity(word, feminist_word) for feminist_word in feminist_words]
            #     print('feminist score:', np.mean([x for x in feminist_similarity if x != -1]))
            #     not_feminist_similarity = [safe_model_similarity(word, not_feminist_word) for not_feminist_word in non_feminist_words]
            #     print('non feminist score:', np.mean([x for x in not_feminist_similarity if x != -1]))
            #
