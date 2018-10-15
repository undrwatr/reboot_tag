#!/usr/bin/python

# SCripts allows HD to elevate their privileges by adding a specific tag to a store. The user must be set with that tag already and full access.

#imports
import requests
import json
import os
import sys
import smtplib
from email.mime.text import MIMEText

#Private credentials file, used to make life easy when I deploy new scripts.
import cred

#custom variables for the program imported from the cred.py file located in the same directory
organization = cred.organization
key = cred.key
hub = cred.hub
me = cred.me
you = cred.you


#Main URL for the Meraki Platform
dashboard = "https://api.meraki.com/api/v0"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

#pulls in the store number from the script that is calling this script
store = sys.argv[1]

#Pull the information from the Meraki cloud to get the network id
#pull back all of the networks for the organization
get_network_id_url = dashboard + '/organizations/%s/networks' % organization

#request the network data
get_network_id_response = requests.get(get_network_id_url, headers=headers)

#puts the data into json format
get_network_id_json = get_network_id_response.json()

#pull back the network_id of the store that you are configuring
for i in get_network_id_json:
    if i["name"] == str(store):
        network_id=(i["id"])

#Update the network, with a predefined list of tags for the Meraki Cloud
UPDATE_NET_JSON = {}
UPDATE_NET_JSON["tags"] = "STORES reboot"

#Create the URL
create_netjsonurl = dashboard + '/networks/%s' % network_id

#perform the update
create_netjson = requests.put(create_netjsonurl, data=json.dumps(UPDATE_NET_JSON), headers=headers)

# Create a text/plain message
#msg = MIMEText(connecting.read())

# me == the sender's email address
# you == the recipient's email address
#msg['Subject'] = 'HD escalated their access to reboot a store'
#msg['From'] = me
#msg['To'] = ', '.join(you)

# Send the message via our own SMTP server, but don't include the
# envelope header.
#s = smtplib.SMTP(cred.email_server)
#s.sendmail(me, you, msg.as_string())
#s.quit()

