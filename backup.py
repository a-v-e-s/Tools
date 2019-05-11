import os, datetime, shutil, pickle, sys

def main():
    # Make sure we are running this as root so that some files are not skipped over:
    if os.geteuid() == 0:
        #pass
    #else:
        print('\nTry again as root!\n')
        input('Press <Enter> to acknowledge')
        exit()

    # Find or create a list of directories to be backed up
    backupList = []
    if os.path.exists('backupList.pkl'):
        with open('backupList.pkl', 'rb') as file:
            backupList = pickle.load(file)
    else:
        with open('backupList.pkl', 'wb') as file:
            while True:
                x = input('\nEnter the full, absolute path of each file or directory you want to backup one at a time.\nPress <Enter> to move to the next directory, or Enter "q" when you are finished:\n')
                if x.lower() == 'q':
                    pickle.dump(backupList, file)
                    break
                elif os.path.isdir(x) or os.path.isfile(x):
                    backupList.append(x)
                else:
                    print('\n', x, 'is not a file or directory!\nPlease try again and make sure you enter the full, absolute path\n')
                    continue

    # Make sure we have all the correct directories on our list 
    print('\nHere is the full list of files and directories to be backed up:\n')
    for x in backupList:
        print(x)
    if input('\nWould you like to make any changes to this list before continuing?\nEnter "y" to make changes:\n').lower() == 'y':
        backupList = modify(backupList)

    # Find or create a general target to make the final backup directory in, save this target in a .pkl file
    basepath = ''
    if os.path.exists('path.pkl'):
        with open('path.pkl', 'rb') as file2:
            basepath = pickle.load(file2)
    else:
        while True:
            basepath = input('\nEnter the full path to the directory you are saving your backups to:\n')
            if os.path.isdir(basepath):
                with open('path.pkl', 'wb') as file2:
                    pickle.dump(basepath, file2)
                    break
            else:
                print('\nYour entry was not a valid directory.\nPlease try again.\n')

    # Finally, the reason we're doing this:
    folderName = str(datetime.datetime.now()).split()[0]
    path = os.path.join(basepath, folderName)
    for x in backupList:
        print('Copying', x)
        if os.path.isdir(x):
            try:
                shutil.copytree(x, path + str(x))
            except: # We stop at nothing because this program is crude and imperfect
                print(sys.exc_info())
        else:
            shutil.copy2(x, path)

def modify(backupList):
    # Create and print a numbered list of each directory on backupList
    numbered = dict(zip(list(range(len(backupList))), backupList))
    input('\nPress <Enter> to see the numbered list of directories and files in your backup list:\n')
    for key in numbered:
        print(key, numbered[key])
    
    # Add and delete until the user is satisfied
    while True:
        x = input('\nEnter the numerical value of the item you would like to remove, or the full path of a file or directory you would like to add to the list:\nEnter "q" to quit\n')
        if x.isdigit() and numbered[int(x)]:
            print('Removing:', numbered[int(x)])
            backupList.remove(numbered[int(x)])
            del numbered[int(x)]
        elif os.path.isdir(x) or os.path.isfile(x):
            backupList.append(x)
            #numbered[???] = x
        elif x.lower() == 'q':
            break
        else:
            print('\nInvalid input, please try again.\n')

    # Make sure we are good to go
    numbered = dict(zip(list(range(len(backupList))), backupList))
    print('\nHere is the updated list of directories to be backed up:\n')
    for key in numbered:
        print(key, numbered[key])
    if input('\nIs this acceptable?\nEnter "y" to accept:\n').lower() == 'y':
        # not 100% sure this will work:
        with open('backupList.pkl', 'wb') as file:
            pickle.dump(backupList, file)
            return backupList
    else:
        modify(backupList)

if __name__ == '__main__':
    main()
