import urllib, json

APIURL = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/geojson?'
addr = raw_input("Enter the location: ")

url = APIURL + urllib.urlencode({'sensor': 'false', 'address': addr})

print "Retrieving", url

try:
    js = json.loads(urllib.urlopen(url).read())
    print "We've got it, Houston!"
except:
    js = None
    print "We've got none. There's a problem"

if js['status'] != "OK" or 'status' not in js:
    print "Operation cancelled. There's a problem"

print "Place id", js['results'][0]['place_id']