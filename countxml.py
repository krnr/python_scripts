import urllib
import xml.etree.ElementTree as ET

url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_193470.xml'

urldata = urllib.urlopen(url).read()
tree = ET.fromstring(urldata)

results = tree.findall('.//count')
summm = sum(int(i.text) for i in results)

print summm
