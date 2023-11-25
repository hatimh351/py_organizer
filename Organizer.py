import os
import OrganizerExceptions
import re
from pathlib import Path

class Organizer:

    ''' 
        "The constructor's purpose is to parse the 'Organizer' file and set all the attributes I need."
    '''
    def __init__(self, file) -> None:
        self.header = ''' 
        |\\         /|   _________                    __               _________
        |  \\      / |       |         |            /    \\    | /          |
        |   \\    /  |       |         |           |      |   |/           |
        |    \\  /   |       |         |            \\    /    |\\           |
        |     \\/    |   ---------     -------        --      | \\      ---------\n\n''' 
    # searching attributes
        self._target = ""
        self._targetPath = ""
        self._searchingStart = ""
    # orginizer attributes
        self._dirsToOrganize00 = ""
        self._done00 = False
        self._dirsToOrganize01 = ""
        self._done01 = False
        self._exts = ""
        self._NewDirName = ""
        self._file = file
        try:
            self.results = open("results.txt", "w")
        except:
            print("Couldn't open the results.txt file")
            self._good = False
            exit(1)
        # we are parsing the file and calling on eache task it's function to parse it  
        self.results.write(self.header)
    # *********************** The monitoring all the tasks *********************** 
    def monitoring(self):
        with open(self._file, 'r') as file:
            task = ["S:", "O:"]
            pars = [self.ParsSearching, self.ParsOrganizer]
            doingTasks = [self.searching, self.organizer]
            for line in file:
                tokens = line.split()
                if len(tokens) == 0:
                    continue
                idx = -1
                try:
                    idx = task.index(tokens[0])
                except:
                    self.results.write("Using of anknown task in the conf file.\n")
                    self._good = False
                    exit(0)
                # we are checking if the parssing throw an exception
                try:
                    pars[idx](tokens)
                except OrganizerExceptions.Parssing:
                    self.results.write("An error occurred while parsing the task {}\n".format(task[idx]))
                    exit(1)
                except OrganizerExceptions.FileDoesntExist:
                    self.results.write("A directory or File in the task {} dosen't exist.\n".format(task[idx]))
                    exit(1)
                except OrganizerExceptions.PathIsNotDir:
                    self.results.write("A Path given in the task {} excpected to be a dirictory but It's a file.\n".format(task[idx]))
                    exit(1)
                except OrganizerExceptions.PermissionDenied:
                    self.results.write("Task {} was attempting to perform an action without having the necessary permission.\n".format(task[idx]))
                    exit(1)
                doingTasks[idx]()
                self.logs()
                self.reset()
    # *********************** The logs methode to write all the results of our tasks *********************** 
    def logs(self):
        # checking if we are in the searching task
        if len(self._target) != 0:
            if len(self._targetPath) == 0:
                self.results.write("We couldn't find the '{}'. :(\n".format(self._target))
            else:
                self.results.write("We find your target '{}' -> '{}'. :)\n".format(self._target, self._targetPath))
        # if the first option success 
        if self._done00 and len(self._dirsToOrganize00) != 0:
            self.results.write("We success organizing The directory '{}' as you want ! :)\n".format(self._dirsToOrganize00))
        if self._done01 and len(self._dirsToOrganize01) != 0:
            self.results.write("We success organizing The directory '{}' as you want ! :)\n".format(self._dirsToOrganize01))
    # *********************** The reset methode to reset the attributes for next task *********************** 
    def reset(self):
        # searching attributes
        self._target = ""
        self._targetPath = ""
        self._searchingStart = ""
        self._find = False
    # orginizer attributes
        self._dirsToOrganize00 = ""
        self._dirsToOrganize01 = ""
        self._exts = ""
        self._NewDirName = ""
        self._done00 = False
        self._done01 = False
    # *********************** The parsser of the Organizer task *********************** 
    def ParsOrganizer(self, tokens):
        if (len(tokens) < 2):
            raise OrganizerExceptions.Parssing
        if len(tokens) == 2:
            if (not os.path.exists(tokens[1])):
                raise OrganizerExceptions.FileDoesntExist
            if (not os.path.isdir(tokens[1])):
                raise OrganizerExceptions.PathIsNotDir
            self._dirsToOrganize00 = tokens[1]
        elif len(tokens) == 4:
            # checking if the path given is a directory
            if (not os.path.exists(tokens[1])):
                raise OrganizerExceptions.FileDoesntExist
            if not os.path.isdir(tokens[1]):
                raise OrganizerExceptions.PathIsNotDir
            # path of dirs to organize
            self._dirsToOrganize01 = (tokens[1])
            # exts that you want group in one directory
            exts = set([ext for ext in tokens[2].split(',')])
            self._exts = exts
            # directory name where you want group all the file with exts you specified
            self._NewDirName = tokens[3]
        else:
            raise OrganizerExceptions.Parssing
            

    # *********************** The Organizer task *********************** 
    def organizer(self):
        if len(self._dirsToOrganize00) != 0:
            os.chdir(self._dirsToOrganize00)
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
                            os.replace(os.path.join(self._dirsToOrganize00, file), os.path.join(self._dirsToOrganize00, os.path.join(extdir, file)))
                self._done00 = True
        if len(self._dirsToOrganize01) != 0:
            try:
                os.chdir(self._dirsToOrganize01)
            except:
                self.results.write("We couldn't accesse this path '{}'.\n".format(self._dirsToOrganize01))
            try:
                os.mkdir(self._NewDirName)
            except FileExistsError:
                pass
            except:
                self.results("Couldn't creat the Directory '{}' in this Path '{}'.\n".format(self._NewDirName, self._dirsToOrganize01))
                return
            for file in os.listdir():
                if os.path.isdir(file):
                    continue
                token = file.split('.')
                if len(token) == 1:
                    continue
                if token[1] in self._exts:
                    os.replace(os.path.join(self._dirsToOrganize01, file), os.path.join(self._dirsToOrganize01, os.path.join(self._NewDirName, file)))
            self._done01 = True
    # *********************** The parsser of the Searching task *********************** 
    def ParsSearching(self, tokens):
        if len (tokens) < 2:
            OrganizerExceptions.Parssing
        self._target = tokens[1]
        if len(tokens) == 2:
            self._searchingStart = Path.home().__str__()
        else:
            if (not os.path.exists(tokens[2])):
                raise OrganizerExceptions.FileDoesntExist
            if not os.path.isdir(tokens[2]):
                raise OrganizerExceptions.PathIsNotDir
            self._searchingStart = tokens[2]
    # *********************** The Searching task *********************** 
    
    def searching(self):
        print("Searching !!\n" * 4, end="")
        # here we are searching
        find = False
        for root, dirs, files in os.walk(self._searchingStart):
            if find == True:
                break
            for file in dirs + files:
                # if we find our target we save it's path and we break
                if file == self._target:
                    self._targetPath = (os.path.join(root, file))
                    find = True
                    break
        if find == False:
            self._targetPath = ("")

    # ***************** the purpose of the Destructor is to write to the file result at the end ,It provides a  summury of what this python program does **************
    def __del__(self):
        self.results.close()