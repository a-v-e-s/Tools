"""
flyswatter.py: utilizes iptables to block ip addresses trying to gain
unauthorized access, as indicated by attempting incorrect passwords 5 
or more times. 

Still under active development.

Written by: Jon David Tannehill
"""

import os, sys, re, socket, collections
global ip_attackers
ip_attackers = []

if os.getuid() != 0:
	print('Try again as root!')
	sys.exit()
elif input('Are you logged in as root? [y/n]\nSimply using sudo will not save the rules generated\n').lower() != 'y':
	sys.exit()


def main(log):
	global ip_attackers
	rules = open('/etc/iptables/rules.v4', 'r')
	for x in rules:
		if re.search('DROP', x):
			for y in x.split():
				if re.search('/32', y):			# this needs to be made more widely applicable
					ip_attackers.append(y[:-3])
	
	failed_attempts = []
	for x in log:
		if re.search('Failed password for', x):
			failed_attempts.append(x)
			continue
		if re.search('Invalid user', x):
			failed_attempts.append(x)
			continue
		if re.search('not allowed because not listed in AllowUsers', x):
			failed_attempts.append(x)
			continue
		if re.search('Did not receive identification string from ', x):
			failed_attempts.append(x)

	ip_suspects = []
	for x in failed_attempts:
		for y in x.split():
			if ip4(y):
				ip_suspects.append(y)
			elif ip6(y):
				ip_suspects.append(y)

	new_attackers = [ip for ip, count in collections.Counter(ip_suspects).items() if count > 4]
	for x in new_attackers:
		if x in ip_attackers:
			new_attackers.remove(x)
			
	print('Blocking attackers now...')
	for x in new_attackers:
		command = 'iptables -I INPUT -s ' + x + ' -j DROP'
		os.popen(command)
		print(x, 'was blocked from gaining access to your computer!')


def ip4(n):
	try:
		socket.inet_pton(socket.AF_INET, n)
		return True
	except socket.error:
		return False

		
def ip6(n):
	try:
		socket.inet_pton(socket.AF_INET6, n)
		return True
	except socket.error:
		return False
		
		
def apache(log):
	global ip_attackers
	rules = open('/etc/iptables/rules.v4', 'r')
	for x in rules:
		if re.search('DROP', x):
			for y in x.split():
				if re.search('/32', y):			# this needs to be made more widely applicable
					ip_attackers.append(y[:-3])	
					
	failed_attempts = []
	for x in log:
		if re.search('.*(\.php).*(\s404\s)', x):
			failed_attempts.append(x)
			
	suspects = []
	for x in failed_attempts:
		possible_ip = x.split()[0]
		if ip4(possible_ip):
			suspects.append(possible_ip)
		elif ip6(possible_ip):
			suspects.append(possible_ip)
		else:
			for y in x.split()[1:]:
				if ip4(y):
					suspects.append(y)
				elif ip6(y):
					suspects.append(y)

	new_attackers = [ip for ip, count in collections.Counter(suspects).items() if count > 12]
	for x in new_attackers:
		if x in ip_attackers:
			new_attackers.remove(x)
			
	print('Blocking attackers now...')
	for x in new_attackers:
		command = 'iptables -I INPUT -s ' + x + ' -j DROP'
		os.popen(command)
		print(x, 'was blocked from gaining access to your computer!')
	

if len(sys.argv) == 1:
	with open('/var/log/auth.log', 'r', encoding='utf8') as log:
		main(log)
	with open('/var/log/auth.log.1', 'r', encoding='utf8') as log:
		main(log)
	with open('/var/log/apache2/access.log', 'r', encoding='utf8') as log:
		apache(log)
	with open('/var/log/apache2/access.log.1', 'r', encoding='utf8') as log:
		apache(log)
elif len(sys.argv) > 1:
	for x in sys.argv[1:]:
		try:
			log = open(x, 'r', encoding='utf8')
		except Exception:
			print('Unable to open', x)
			continue
		main(log)	

os.popen('iptables-save > /etc/iptables/rules.v4')
print('\nSuccess!\n')
