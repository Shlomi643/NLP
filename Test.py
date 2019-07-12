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
feminist_words = ['Strong','tough','protective','hero','powerful','aggressive','smart','intelligent','books','independent','leader','mangaer','active','arrogant','dominant']


def safe_model_similarity(x, y):
    try:
        return model.similarity(x, y)
    except KeyError:
        return -1

if __name__ == '__main__':
    my_movie = mmm('Frozen')
    words = my_movie('char_tokens')('Elsa')
    filtered_sentence = [w for w in words if w not in stop_words]
    print([(safe_model_similarity(x, y)) for x, y in itertools.product(filtered_sentence, feminist_words)])

    # for word in filtered_sentence:
    #     print('word:', word)
    #     print('feminist score:', np.mean([safe_model_similarity(word, feminist_words) for feminist_word in feminist_words]))
    #     print('non_feminist score:', np.mean([safe_model_similarity(word, feminist_words) for feminist_word in non_feminist_words]))

        # for name in utils.names:
    #     my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
    #     print(name)
    #     print(my_movie.get_tokens())
    #     print(my_movie.get_characters())
    #     for char in my_movie.get_characters():
    #         pass
            # print(char)
            # print(my_movie.get_char_tokens(char))
