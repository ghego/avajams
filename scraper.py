from bs4 import BeautifulSoup
import requests
import re
import json

#tester link
starting_link = 'http://fmusictv.com/2016/03/shakira-try-everything.html'

url_start = 'http://fmusictv.com/tag/'

link_poss = 'href="http://fmusictv.com/2'

data_file = 'data/artists.json'


artist_names = ['shakira','beyonce']


def parse_list(list,input):
    #parse list
    print 'parsing'
    temp_list = []
    for i in list:
        if i.startswith(input):
            x = re.findall(r'"([^"]*)"', i)
            temp_list.append(x[0])
    print 'parsed'
    return temp_list



def parse_for_video(list,input):
    
    print 'parsing for video'
    temp_list = []
    for i in list:
        if i.startswith(input):
            temp_list.append(re.findall(r'"([^"]*)"', i))
    print 'parsed!'
    return temp_list



def parse_for_genre(inputlist):
    
    print 'parsing for genre'
    for i in inputlist:
        if i.startswith('rel="tag"'):# ='rel="tag">Pop</a></li>\n</ul>\n<div'
            t = ((i.split('>'))[1].split('<')[0])
    print 'parsed!'
    return t



def get_all_artist_links(initial_url):
    print 'getting artist links'

    '''returns a list of all artist links'''

    req =  requests.get(initial_url)
    soup = BeautifulSoup(req.text,'html.parser')
    content = str(soup.findAll('div')).split(' ')

    artist_links = parse_list(content,link_poss)
    arist_links = set(artist_links)
    return artist_links



def get_information(artist, url):
    print 'getting information'
    temp_dict = {}
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    '''pass in soup link from list '''
    text = soup.findAll('div',{'class':'video-container'})
    text_list = str(text).split(' ')
    video = parse_for_video(text_list,'src="https://www.youtube.com/')[0]



    temp_dict['Link'] = video[0]


    other_text = str(soup.findAll('div')).split(' ')
    temp_dict['Genre'] = parse_for_genre(other_text)

    temp_dict['Artist'] = artist
    json.dumps(temp_dict,'data/data.json')
    print 'success!!!'
    return temp_dict


def main():
    for artist in artist_names:
        print 'getting %s' % artist
        new_url = url_start + artist
        try:
            artist_links = get_all_artist_links(new_url)
            for links in artist_links:
                print 'getting links!'
                print links
                try:
                    content = get_information(artist,links)
                    print '**********Content written successfully**********'
                except:
                    print 'failed writeout'
                    pass
        except:
            print 'artist not found on website!'



if __name__ == '__main__':
    print main()
    # print get_information('Shakira',starting_link)
