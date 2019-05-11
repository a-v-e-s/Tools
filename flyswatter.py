"""
flyswatter.py: utilizes iptables to block ip addresses trying to gain
unauthorized access, as indicated by attempting incorrect passwords 5 
or more times. To make these rules persistent requires the
iptables-persistent package.

Support for blocking ipv6 addresses and computers from the same network
is in development

Written by: Jon David Tannehill
"""

import os, re, sys, collections

if os.getuid() != 0:
	print('Try again as root!')
	sys.exit()

log = open('/var/log/auth.log', 'r')
ip4_pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
# ip6_pattern = re.compile("???????????")
failed_attempts = []
suspects = []
attackers = []

for x in log:
	if re.search('Failed password for', x):
		failed_attempts.append(x)

for x in failed_attempts:
	for y in x.split():
		if re.search(ip4_pattern, y):
			suspects.append(y)
		# elif re.search(ip6_pattern, y):
			# suspects.append(y)

attackers = [ip for ip, count in collections.Counter(suspects).items() if count > 4]

print('Blocking attackers now...')
for x in attackers:
	command = 'sudo iptables -I INPUT -s ' + x + ' -j DROP'
	os.popen(command)
	print(x, 'was blocked from gaining access to your computer!')

os.popen('sudo iptables-save | sudo tee /etc/iptables/rules.v4')
# os.popen((command to clear /var/log/auth.log))
print('Success!')
