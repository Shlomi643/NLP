
class Utils:
    filesMap = {}
    names = []
    num_of_formatters = 6

    def __init__(self):
        Utils.init_map()

    @staticmethod
    def set_s(format_index, name):
        return format_index, open("Scripts/Format " + format_index + "/" + name + ".html").read()

    @staticmethod
    def init_map():
        for movie in Utils.data['movies']:
            Utils.names.append(movie['name'])
            Utils.filesMap[movie['name']] = Utils.set_s(movie['formatter'], movie['name'])

    @staticmethod
    def script(name):
        return Utils.filesMap[name][1]

    @staticmethod
    def formatter(name):
        return Utils.filesMap[name][0]

    @staticmethod
    def get_token(line):
        def rpl(y): return line.replace(y, ' ')

        for x in [',', '.', ';', '?', '!', '/']:
            line = rpl(x)
        return line.split()

    data = {
        'movies': [
            {
                'name': 'Cars 2',
                'year': 2011,
                'formatter': '1',
                'source': 'https://www.imsdb.com/scripts/Cars-2.html'
            },
            {
                'name': 'Frozen',
                'year': 2013,
                'formatter': '1',
                'source': 'https://www.imsdb.com/scripts/Frozen-(Disney).html'
            },
            {
                'name': 'Toy Story',
                'year': 1995,
                'formatter': '1',
                'source': 'https://www.imsdb.com/scripts/Toy-Story.html'
            },
            {
                'name': 'Zootopia',
                'year': 2016,
                'formatter': '1',
                'source': 'https://www.imsdb.com/scripts/Zootopia.html'
            },
            {
                'name': 'Aladdin',
                'year': 1992,
                'formatter': '2',
                'source': 'http://www.fpx.de/fp/Disney/Scripts/Aladdin.txt'
            },
            {
                'name': 'Beauty and the Beast',
                'year': 1991,
                'formatter': '2',
                'source': 'https://www.imsdb.com/scripts/Beauty-and-the-Beast.html'
            },
            {
                'name': 'Hercules',
                'year': 1997,
                'formatter': '2',
                'source': 'http://www.cubbi.org/disney/scripts/hercules.txt'
            },
            {
                'name': 'Jungle Book',
                'year': 1967,
                'formatter': '2',
                'source': 'http://www.cubbi.org/disney/scripts/tjb.txt'
            },
            {
                'name': 'Sleeping Beauty',
                'year': 1959,
                'formatter': '2',
                'source': 'http://www.fpx.de/fp/Disney/Scripts/SleepingBeauty/sb.html'
            },
            {
                'name': '101 Dalmatians',
                'year': 1961,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/101_Dalmatians_(1961)'
            },
            {
                'name': 'Brave',
                'year': 2012,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/Brave'
            },
            {
                'name': 'Cars',
                'year': 2006,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/Cars'
            },
            {
                'name': 'Dumbo',
                'year': 1941,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/Dumbo'
            },
            {
                'name': 'Inside Out',
                'year': 2015,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/Inside_Out'
            },
            {
                'name': 'Moana',
                'year': 2016,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/Moana'
            },
            {
                'name': 'The Aristocrats',
                'year': 1970,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/The_Aristocats'
            },
            {
                'name': 'Toy Story 2',
                'year': 1999,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/Toy_Story_2'
            },
            {
                'name': 'Toy Story 3',
                'year': 2010,
                'formatter': '3',
                'source': 'https://transcripts.fandom.com/wiki/Toy_Story_3'
            },
            {
                'name': 'Mulan',
                'year': 1998,
                'formatter': '4',
                'source': 'http://www.fpx.de/fp/Disney/Scripts/Mulan.html'
            },
            {
                'name': 'The Little Mermaid',
                'year': 1989,
                'formatter': '4',
                'source': 'https://www.imsdb.com/scripts/Little-Mermaid,-The.html'
            },
            {
                'name': 'Pocahontas',
                'year': 1995,
                'formatter': '5',
                'source': 'https://transcripts.fandom.com/wiki/Pocahontas'
            },
            {
                'name': 'Alice in Wonderland',
                'year': 1951,
                'formatter': '6',
                'source': 'https://transcripts.fandom.com/wiki/Alice_in_Wonderland_(1951)'
            },
            {
                'name': 'Finding Nemo',
                'year': 2003,
                'formatter': '6',
                'source': 'https://transcripts.fandom.com/wiki/Finding_Nemo'
            },
            {
                'name': 'Toy Story 4',
                'year': 2019,
                'formatter': '6',
                'source': 'https://disneyfanon.fandom.com/wiki/Toy_Story_4_transcript'
            },
        ]
    }
