#!/usr/local/bin/python3

import os, sys

def pull(path, directory):
	os.chdir(path)

	attempt = 1
	while attempt < 3:
		if 'LICENSE.md' in os.listdir():
			command = 'git pull --repo=https://github.com/a-v-e-s/' + directory
			try:
				os.popen(command)
			except Exception:
				print('\nTried pulling from https://github.com/a-v-e-s/' + directory, 'but failed.')
				print('Exeption info:')
				print(sys.exc_info())
            else:
                print('git pull was successful for', directory)
			finally:
				break
		elif 'PRIVATE_FILE.txt' in os.listdir():
			command = 'git pull --repo=http://jondavid.ddns.net:/srv/git/' + directory
			try:
				os.popen(command)
			except Exception:
				print('\nTried pulling from http://jondavid.ddns.net:/srv/git/' + directory, 'but failed.')
				print('Exeption info:')
				print(sys.exc_info())
            else:
                print('git pull was successful for', directory)
			finally:
				break
		else:
			os.popen('git checkout master')
			attempt += 1


if __name__ == '__main__':
    path = sys.argv[1]
    directory = sys.argv[1].split('/')[-1]
    pull(path, directory)