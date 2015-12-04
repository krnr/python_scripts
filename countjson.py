import urllib, json

#url = raw_input('Enter url: ')
url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_193474.json'

js = json.loads(urllib.urlopen(url).read())
print sum(int(i['count']) for i in js['comments'])