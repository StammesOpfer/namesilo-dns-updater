# namesilo-dns-updater

Barebones script for Namesilo dynamic dns updates

Quick and dirty script to update a DNS record on NameSilo based on current IP address

Originally from: http://vivithemage.com/2018/09/17/namesilo-dns-update-via-python-script-and-cron-job-on-pfsense/

Modified by: Matthew Reishus (2019-08-14)
Modified by: StammesOpfer (2022-06-28)

Updated to remove requirment to install request module.

# Instructions
1. Update file with you domain info and NameSilo api key.
2. Copy it to you pfsense and chmod +x it.
3. Install the cron add-on and schdule a job to run the script.
