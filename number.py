"""
number.py: A crude script for numbering and renaming the files in one or more directories
Written by: Jon David Tannehill
"""

import os, sys, argparse


def main(repeat=0):
    directory_list = []
    extensions = []

    if len(sys.argv) == 1 or repeat:
        directory_list = [x for x in input('\nEnter the directory or directories whose files you want to number separated by spaces:\n').split() if os.path.isdir(x)]
        extensions = [x for x in input('\nEnter a space-separated list of the extensions for the file types you wish to have numbered Leave blank to include all files:\n').split() if len(x) > 0]
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('directories', type=str, nargs='*', metavar='/path/to/directory1 /path/to/directory2', help='Enter a space-separated list of the full paths to directories whose files you wish to have numbered')
        parser.add_argument('-e', action='store', dest='e', nargs='*', help='Optionally, enter a space separated-list of the file extensions whose files you wish to have numbered.\nExample:\njpg wmv mp4 mp3 doc')

        args = parser.parse_args()
        for x in args.directories:
            if os.path.isdir(x):
                directory_list.append(x)
            else:
                print(x, 'is not a directory.')
        if args.e != None:
            for x in args.e:
                extensions.append(x)

    for x in directory_list:

        files_to_number = []
        for y in os.listdir(x):
            if len(extensions) > 0:
                for z in extensions:
                    if y.endswith(z):
                        files_to_number.append(y)
                        break
            else:
                files_to_number.append(y)

        already_done = []
        for a in files_to_number:
            try:
                name = int(str(a.split('.')[:1]).strip("[']"))
                if name in range(1, len(files_to_number)):
                    already_done.append(a)
                    continue
            except ValueError:
                pass

        for a in already_done:
            files_to_number.remove(a)

        os.chdir(x)
        index = 1
        for a in files_to_number:
            while True:
                new_name = str(index) + '.' + str(a.split('.')[-1:]).strip("[']")
                if new_name in already_done:
                    index += 1
                else:
                    break
            
            command = 'mv "' + a + '" ' + new_name
            os.popen(command)
            print('Renamed', a, 'to', new_name)
            index += 1

    if input('\nGo again? [y/n]\n').lower() == 'y':
        main(repeat=1)


if __name__ == '__main__':
    main()
