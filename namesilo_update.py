#!/usr/bin/env python3.8
# May need to update python version 3.8 is current as of pfsense 2.6

# Quick and dirty script to update a DNS record on NameSilo based on current IP address
# Originally from: http://vivithemage.com/2018/09/17/namesilo-dns-update-via-python-script-and-cron-job-on-pfsense/
# Modified by: Matthew Reishus (2019-08-14)
# Modified again by: StammesOpfer (2022-06-28)

# Usage:  Change the variables at the top of the script
# Then run it, either on cron or driven by some event
#   - Checks current external IP address and the IP address of the specified domain
#     - If match, no action taken
#     - If no match, update the domain to my current (external) IP address

import subprocess
import xml.etree.ElementTree as ET

# To update 'home.example.com', set SUB to 'home' and DOMAIN to 'example.com'
SUB    = 'home'
DOMAIN = 'example.com'
FULL   = SUB + '.' + DOMAIN
KEY    = '1234567890abcdef12345'

RECORD_IP_ADDRESS_URL  = 'https://www.namesilo.com/api/dnsListRecords?version=1&type=xml&key=' + KEY + '&domain=' + DOMAIN
CURRENT_IP_ADDRESS_URL = 'http://whatismyip.akamai.com/'

# get current IP address
current = subprocess.check_output(['curl', '-sL', CURRENT_IP_ADDRESS_URL]).decode("utf-8")


# look up domain records from namesilo
r = subprocess.check_output(['curl', '-s', RECORD_IP_ADDRESS_URL])
xml = ET.fromstring(r)

for record in xml.iter('resource_record'):
    host = record.find('host').text
    value = record.find('value').text
    record_id = record.find('record_id').text

    # look for the correct host
    if (host == FULL):
        print(FULL + ' record IP address: %s' % value)

        # do we need to update?
        if (value == current):
            print('Current IP address matches namesilo record')
        else:
            print('IP addresses do not match, generating URL to update')

            # make update url
            new_URL = 'https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=xml&key=' + KEY + '&domain=' + DOMAIN + '&rrid='+record_id+'&rrhost=' + SUB + '&rrvalue='+current+'&rrttl=3600'
            print(new_URL)

            # send request, print response
            new = subprocess.check_output(['curl', '-s', new_URL]).decode("utf-8")
            print(new)
