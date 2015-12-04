import urllib
from BeautifulSoup import *

count = int(raw_input("Enter count: "))
pos = int(raw_input("Enter position: "))

url = "http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/known_by_Roshni.html"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

# Retrieve all of the anchor tags
tags = soup('a')

for i in range(0, count):
   print tags[pos - 1].contents[0]
   url = tags[pos - 1].get('href')
   html = urllib.urlopen(url).read()
   soup = BeautifulSoup(html)
   tags = soup('a')
