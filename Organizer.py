import os
from pathlib import Path
import OrganizerExceptions
import re

class Organizer:

    ''' 
        "The constructor's purpose is to parse the 'Organizer' file and set all the attributes I need."
    '''
    def __init__(self, file) -> None:
    # bool to check that every thing went good 
        self._good = True
    # searching attributes
        self._targets = []
        self._targetPath = []
        self._searchingStart = []
        self._find = False
    # orginizer attributes
        self._dirsToOrganize00 = []
        self._dirsToOrganize01 = []
        self._exts = []
        self._NewDirName = []
        # we are parsing the file and calling on eache task it's function to parse it  
        with open(file, 'r') as file:
            task = ["S:", "O:"]
            pars = [self.ParsSearching, self.ParsOrganizer]
            
            for line in file:
                tokens = line.split()
                if len(tokens) == 0:
                    continue
                idx = -1
                try:
                    idx = task.index(tokens[0])
                except:
                    print("Using of anknown task")
                    self._good = False
                    exit(0)
                # we are checking if the parssing throw an exception
                try:
                    pars[idx](tokens)
                except OrganizerExceptions.Parssing:
                    print("An error occurred while parsing the task {}".format(task[idx]))
                    self._good = False
                    exit(1)
                except OrganizerExceptions.FileDoesntExist:
                    print("A directory or File in the task {} dosen't exist.".format(task[idx]))
                    self._good = False
                    exit(1)
                except OrganizerExceptions.PathIsNotDir:
                    print("A Path given in the task {} excpected to be a dirictory but It's a file.".format(task[idx]))
                    self._good = False
                    exit(1)
                except OrganizerExceptions.PermissionDenied:
                    print("Task {} was attempting to perform an action without having the necessary permission.".format(task[idx]))
                    exit(1)

    # *********************** The parsser of the Organizer task *********************** 
    def ParsOrganizer(self, tokens):
        if (len(tokens) < 2):
            raise OrganizerExceptions.Parssing
        if len(tokens) == 2:
            if (not os.path.exists(tokens[1])):
                raise OrganizerExceptions.FileDoesntExist
            if (not os.path.isdir(tokens[1])):
                raise OrganizerExceptions.PathIsNotDir
            self._dirsToOrganize.append(tokens[1])
        elif len(tokens) == 4:
            # checking if the path given is a directory
            if (not os.path.exists(tokens[1])):
                raise OrganizerExceptions.FileDoesntExist
            if not os.path.isdir(tokens[1]):
                raise OrganizerExceptions.PathIsNotDir
            # path of dirs to organize
            self._dirsToOrganize01.append(tokens[1])
            # exts that you want group in one directory
            exts = set([ext for ext in tokens[2].split(',')])
            self._exts.append(exts)
            # directory name where you want group all the file with exts you specified
            self._NewDirName.append(tokens[3])
        else:
            raise OrganizerExceptions.Parssing
            

    # *********************** The Organizer task *********************** 
    def organizer(self):
        for dir in self._dirsToOrganize00:
            os.chdir(dir)
            files = [file for file in os.listdir() if os.path.isfile(file)]
            ext = set()
            for file in files:
                token = file.split('.')
                if len(token) == 2:
                    ext.add(token[1])
            for subdir in ext:
                try:
                    os.mkdir(subdir)
                except PermissionError:
                    raise OrganizerExceptions.FileDoesntExist
                except:
                    continue

            for extdir in ext:
                pattern = ".{}$".format(extdir)
                for file in files:
                    if re.search(pattern, file) != None:
                        os.replace(os.path.join(dir, file), os.path.join(dir, os.path.join(extdir, file)))
        
        for dir,newDir,ext in zip(self._dirsToOrganize01, self._NewDirName, self._exts):
            try:
                os.chdir(dir)
            except:
                print("We couldn't accesse this path '{}'.".format(dir))
            try:
                os.mkdir(newDir)
            except FileExistsError:
                pass
            except:
                print("Couldn't creat the Directory '{}' in this Path '{}'.".format(newDir, dir))
                continue
            for file in os.listdir():
                if os.path.isdir(file):
                    continue
                token = file.split('.')
                if len(token) == 1:
                    continue
                if token[1] in ext:
                    os.replace(os.path.join(dir, file), os.path.join(dir, os.path.join(newDir, file)))
            
            
    # *********************** The parsser of the Searching task *********************** 
    def ParsSearching(self, tokens):
        if len (tokens) < 2:
            OrganizerExceptions.Parssing
        self._targets.append(tokens[1])
        if len(tokens) == 2:
            self._searchingStart.append(Path.home().__str__())
        else:
            if (os.path.exists(tokens[2])):
                self._searchingStart.append(tokens[2])
            # if the path doesn't exist
            else:
                raise OrganizerExceptions.FileDoesntExist
    # *********************** The Searching task *********************** 
    
    def searching(self) -> None:
        print("Searching !!\n" * 4, end="")
        # here we are searching
        
        for searchingStart, target in zip(self._searchingStart, self._targets):
            find = False
            for root, dirs, files in os.walk(searchingStart):
                if find == True:
                    break
                for file in dirs + files:
                    # if we find our target we save it's path and we break
                    if file == target:
                        self._targetPath.append(os.path.join(root, file))
                        find = True
                        break
            if find == False:
                self._targetPath.append("")

    # ***************** the purpose of the Destructor is to write to the file result at the end ,It provides a  summury of what this python program does **************
    def __del__(self):
        header = ''' 
                        |\\         /|   _________                    __               _________
                        |  \\      / |       |         |            /    \\    | /          |
                        |   \\    /  |       |         |           |      |   |/           |
                        |    \\  /   |       |         |            \\    /    |\\           |
                        |     \\/    |   ---------     -------        --      | \\      ---------
        ''' 

        with open("results.txt", 'w') as results:
            results.write(header)
            # if (not self._good):
            #     return
            # for target,path in zip(self._targets, self._targetPath):
            #     if (len(path)):
            #         print("The {} was found their path is {}".format(target, path))
            #     else:
            #         print("The {} wasn't found".format(target))