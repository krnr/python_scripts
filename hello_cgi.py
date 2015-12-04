#!/usr/bin/python
import cgi

print ("Content-type: text/html\r\n\r\n")
print ("<html><body>")
print("<h1>It works CGI!!!!!!!</h1>")

form = cgi.FieldStorage()
if form.getvalue('user'):
	name = form.getvalue('user')
	print ("<h1>Hello %s! Thanks for coming</h1><br />" % name)
if form.getvalue('happy_cbox'):
	print ("<p>I'm happy too!</p>")
if form.getvalue('sad_cbox'):
	print ("<p>Why so sad?</p>")

print ("<form method='post' action = 'hello.py'>")
print ("<p>Name: <input type='text' name='user' /></p>")
print ("<p><input type='checkbox' name='happy_cbox' /> Happy</p>")
print ("<p><input type='checkbox' name='sad_cbox' /> Sad</p>")
print ("<p><input type='submit' value='Submit' /></p>")
print ("</body></html>")