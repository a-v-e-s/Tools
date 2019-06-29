#!/usr/local/bin/python3

import cgitb; cgitb.enable()
import cgi

form_data = cgi.FieldStorage()
name = form_data.getvalue('name')
contact_info = form_data.getvalue('contact')
message = form_data.getvalue('message')

with open('latest.txt', 'w') as info:
    info.write(name + '\n')
    info.write(contact_info + '\n')
    info.write(message + '\n')
