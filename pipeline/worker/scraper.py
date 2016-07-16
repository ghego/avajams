from bs4 import BeautifulSoup
import requests
import re
import json
from data.top_mtv_artists import artist_names

# tester link
starting_link = 'http://fmusictv.com/2016/03/shakira-try-everything.html'

url_start = 'http://fmusictv.com/tag/'

link_poss = 'href="http://fmusictv.com/2'

data_file = 'data/artists.json'


# artist_names = ['beyonce','billy-joel','skrillex']


def json_to_pandas(filename):
    with open(filename) as f:
        data = f.readlines()
    data = map(lambda x: x.rstrip(), data)
    data_json_str = "[" + ','.join(data) + "]"
    return pd.read_json(data_json_str, orient=records)


def parse_list(input_list, input):
    # parse list
    print 'parsing'
    temp_list = []
    for i in input_list:
        if i.find(input) != -1:
            x = re.findall(r'"([^"]*)"', i)
            temp_list.append(x[0])
    print 'parsed'
    return temp_list


def parse_for_video(input_list, input):

    temp_list = []
    for i in input_list:
        if i.find(input) != -1:
            temp_list.append(re.findall(r'"([^"]*)"', i))
    return temp_list


def parse_for_genre(inputlist):

    for i in inputlist:
        if i.startswith('rel="tag"'):  # ='rel="tag">Pop</a></li>\n</ul>\n<div'
            t = ((i.split('>'))[1].split('<')[0])
    return t


def get_all_artist_links(initial_url):
    print 'getting artist links'

    '''returns a list of all artist links'''

    req = requests.get(initial_url)
    soup = BeautifulSoup(req.text, 'html.parser')
    content = str(soup.findAll('div')).split(' ')

    artist_links = parse_list(content, link_poss)
    arist_links = set(artist_links)
    return artist_links


def get_information(artist, url):
    print 'getting information'
    temp_dict = {}
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    '''pass in soup link from list '''
    text = soup.findAll('div', {'class': 'video-container'})
    text_list = str(text).split(' ')
    video = parse_for_video(text_list, 'www.youtube.com/')[0]

    # video = parse_for_video(text_list,'src="//www.youtube.com/')[0]

    temp_dict['Link'] = video[0]

    other_text = str(soup.findAll('div')).split(' ')
    temp_dict['Genre'] = parse_for_genre(other_text)

    temp_dict['Artist'] = artist
    outfile = open('data/data.json', 'a')
    json.dump(temp_dict, outfile)
    outfile.write('\n')
    # print 'success!!!'
    return temp_dict


def main():
    for artist in artist_names:
        print 'getting %s' % artist
        new_url = url_start + artist
        try:
            artist_links = get_all_artist_links(new_url)
            for links in artist_links:
                print links
                try:
                    get_information(artist, links)
                    print '**********Content written successfully**********'
                except:
                    print 'failed writeout'
                    pass
        except:
            print 'artist  not found on website!'


if __name__ == '__main__':
    main()
    # print get_information('Shakira',starting_link)
