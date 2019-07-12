from Utilities import Data
from FF import FirstFormatter
from SF import SecondFormatter

utils = Data()
for name in utils.names:
    my_movie = FirstFormatter(name) if Data.formatter(name) == 'First' else SecondFormatter(name)
    print(name)
    print(my_movie.get_tokens())
    print(my_movie.get_characters())
    for char in my_movie.get_characters():
        pass
        # print(char)
        # print(my_movie.get_char_tokens(char))
