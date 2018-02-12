import argparse
from pprint import pprint
from prettytable import PrettyTable

from .cache.movie import MovieCache
from .cache.download import DownloadCache
from .apis.douban import DoubanAPI
from .apis.movie_heaven import MovieHeavenAPI
from .recommend import recommend
from .logger import logger

desc = "Recommend && Find && Download Movie cli"
version_info = """
                                         ____                                              
            .--.,        ,---,         ,'  , `.                         ,--,               
  __  ,-. ,--.'  \     ,---.'|      ,-+-,.' _ |    ,---.              ,--.'|               
,' ,'/ /| |  | /\/     |   | :   ,-+-. ;   , ||   '   ,'\       .---. |  |,                
'  | |' | :  : :       |   | |  ,--.'|'   |  ||  /   /   |    /.  ./| `--'_        ,---.   
|  |   ,' :  | |-,   ,--.__| | |   |  ,', |  |, .   ; ,. :  .-' . ' | ,' ,'|      /     \  
'  :  /   |  : :/|  /   ,'   | |   | /  | |--'  '   | |: : /___/ \: | '  | |     /    /  | 
|  | '    |  |  .' .   '  /  | |   : |  | ,     '   | .; : .   \  ' . |  | :    .    ' / | 
;  : |    '  : '   '   ; |:  | |   : |  |/      |   :    |  \   \   ' '  : |__  '   ;   /| 
|  , ;    |  | |   |   | '/  ' |   | |`-'        \   \  /    \   \    |  | '.'| '   |  / | 
 ---'     |  : \   |   :    :| |   ;/             `----'      \   \ | ;  :    ; |   :    | 
          |  |,'    \   \  /   '---'                           '---"  |  ,   /   \   \  /  
          `--'       `----'                                            ---`-'     `----'   
Recommend && Find && Download Movie Cli
version 0.1.1
"""
HEADERS = ("name", "rate", "rate_num", "countries", "director", "types", "douban_url")


def rfd_movie(movie_name, page_size=5, pos=0, output='./', action="find", cache=True):
    if action == "find":
        if cache:
            return MovieCache.read(movie_name, num=page_size)
        else:
            return DoubanAPI.read(movie_name, num=page_size)
    elif action == "download":
        if cache:
            return DownloadCache.read(movie_name, num=page_size)
        else:
            return MovieHeavenAPI.read(movie_name, num=page_size)
    elif action == "recommend":
        return recommend(movie_name)
    else:
        print("Unsupported action: {}".format(action))


def show(movies, color=True):
    if not color:
        pprint(movies)
    else:
        movie_list = [[colored("red", str(movie[header])) for header in HEADERS] for movie in movies]
        pretty_print(movie_list)


def colored(color, text):
    '''shell下的颜色处理'''
    table = {
        'red': '\033[91m',
        'green': '\033[92m',
        # no color
        'nc': '\033[0m'
    }
    cv = table.get(color)
    nc = table.get('nc')
    return ''.join([cv, text, nc])


def pretty_print(movies):
    pt = PrettyTable()
    pt._set_field_names(HEADERS)
    for movie in movies:
        pt.add_row(movie)
    print(pt)


def main():
    parse = argparse.ArgumentParser(description=desc)
    parseGroup = parse.add_argument_group()
    parseGroup.add_argument("-f", "--find", action="store_true", help="search mode")
    parseGroup.add_argument("-d", "--download", action="store_true", help="download mode")
    parseGroup.add_argument("-r", "--recommend", action="store_true", help="recommend mode")
    parse.add_argument("-v", "--version", action="store_true", help="print product version")
    parse.add_argument("-n", "--num", type=int, default=5, help="number of movies to return, default is 5")
    parse.add_argument("-p", "--pos", type=int, default=0, help="position for movie list to select")
    parse.add_argument("-o", "--output", type=str, default="./", help="path to output your movie")
    parse.add_argument("-g", "--page", type=int, default=1, help="the page you want to change")
    parse.add_argument("-c", "--color", action="store_true", help="enable colorized output")
    parse.add_argument("-C", "--cache", action="store_true", help="using the cache")
    parse.add_argument("-m", "--movie", type=str, help="the movie names you want to rfd")
    args = parse.parse_args()

    if args.version:
        print(version_info)

    if args.find:
        logger.info("find MovieName: " + args.movie)
        movies = rfd_movie(args.movie, args.num, args.pos, args.output, action="find", cache=args.cache)
        show(movies, color=args.color)
    elif args.download:
        logger.info("download MovieName: " + args.movie)
        rfd_movie(args.movie, args.num, args.pos, args.output, action="download", cache=args.cache)
    elif args.recommend:
        logger.info("recommend MovieName: " + args.movie)
        rfd_movie(args.movie, args.num, args.pos, args.output, action="recommend", cache=args.cache)


if __name__ == "__main__":
    main()
