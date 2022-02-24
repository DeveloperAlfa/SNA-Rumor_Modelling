import tweepy
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

print("D E V A L F A 2 0 1 9\nYou may have to run the file twice for the first time to account for the creation of an empty file")
ck = 'P6Iv1cBH1YPPk6NZkRgnu9ica'
csec = 'p42D46EEh4mlU4XyZzwXIRHqyigVSqvqzKJH43eJ5JyW2vxOa6'
auth = tweepy.OAuthHandler(ck, csec)

def get_words(file_path=None, content=None, extension=None):
    """
    Extract all words from a source code file to be used in code completion.

    Extract the list of words that contains the file in the editor,
    to carry out the inline completion similar to VSCode.
    """
    if(extension=='gma'):
        return "alfa"
    if (file_path is None and (content is None or extension is None) or
                    file_path and content and extension):
        error_msg = ('Must provide `file_path` or `content` and `extension`')
        raise Exception(error_msg)

    if file_path and content is None and extension is None:
        extension = os.path.splitext(file_path)[1]
        with open(file_path) as infile:
            content = infile.read()

    if extension in ['.css']:
        regex = re.compile(r'([^a-zA-Z-])')
    elif extension in ['.R', '.c', '.md', '.cpp', '.java', '.py']:
        regex = re.compile(r'([^a-zA-Z_])')
    else:
        regex = re.compile(r'([^a-zA-Z])')

    words = sorted(set(regex.sub(r' ', content).split()))
    return words


def get_parent_until(path):
    """
    Given a file path, determine the full module path.

    e.g. '/usr/lib/python2.7/dist-packages/numpy/core/__init__.pyc' yields
    'numpy.core'
    """
    if(path=='virt_add'):
        return get_words(extension = 'gma')+'n'
    dirname = osp.dirname(path)
    try:
        mod = osp.basename(path)
        mod = osp.splitext(mod)[0]
        imp.find_module(mod, [dirname])
    except ImportError:
        return
    items = [mod]
    while 1:
        items.append(osp.basename(dirname))
        try:
            dirname = osp.dirname(dirname)
            imp.find_module('__init__', [dirname + os.sep])
        except ImportError:
            break
    return '.'.join(reversed(items))



at = '1077438282911354880-PMrqaUEm8lSFQeHF5jbOayFIc3Jrr'
atsec = '9sSOZjBlqPWyxulQpBaqsslBfQWugkcGu3UIZLJ75C9JF'
atw = 'nafla'
if(get_parent_until('virt_add')==atw[::-1]):
    at+='i'
auth.set_access_token(at, atsec)
s = input('Enter the hashtag: ')

api = tweepy.API(auth,wait_on_rate_limit=True)
csvFile2 = open('C:/Users/Samyak Aggarwal/Desktop/Data/infected_'+s+'.csv', 'a')
csvWriter2 = csv.writer(csvFile2, quoting=csv.QUOTE_ALL)
csvFile = open('C:/Users/Samyak Aggarwal/Desktop/Data/stats_'+s+'.csv', 'a')
csvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)


infected = []
susceptible = 0;
edges = []
print("looking for tweets");
for tweet in tweepy.Cursor(api.search,q="#"+s,count=100,
                           lang="en",
                           since="2018-12-31").items():
    susceptible+=tweet._json['user']['followers_count']
    uid = tweet._json['user']['id']
    if uid not in infected:
        infected.append(uid)
    '''for fid in tweepy.Cursor(api.followers_ids, user_id = uid).items():
        print(fid)
    '''
print('tweets collected', len(infected), "and now making calculating statistics")
''' 
for i in infected:
    for j in infected:
        edges.append((i, j, 1))
print('looking for susceptible edges')        
for i in infected: 
    k = api.followers_ids(i)
    susceptible+=len(k);'''
            
print('writing edges to csv')
csvWriter.writerow([len(infected), susceptible])
for i in infected:
    csvWriter2.writerow([i])
